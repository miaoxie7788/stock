"""
    Scan candlestick patterns.
"""

import os
import re
from datetime import datetime, timedelta

import pandas as pd

from candlestick.core.signal import is_hammer_signal
from stock_market_data.yahoo import get_stock_historical_data


def get_data(watchlist="hs_watchlist", market="hs_stock", last_days=21, path="data/candlestick"):
    """
        Get historical data for stocks presented in the watchlist between today and today-last_days.
        Note, last_days should be larger than his_size.
    """

    # Read watchlist.
    watchlist_path = os.path.join(path, watchlist)
    with open(watchlist_path) as f:
        stock_codes = [line.strip() for line in f.readlines()]

    data_path = os.path.join(path, market)
    if not os.path.exists(data_path):
        os.mkdir(data_path)

    today = datetime.today()
    start_date = today - timedelta(days=last_days)
    end_date = today + timedelta(days=1)

    for stock_code in stock_codes:
        get_stock_historical_data(stock_code=stock_code, start_date=start_date, end_date=end_date, path=data_path)


def scan_daily_hammer_signal(params, watchlist="hs_stock_codes", market="hs_stock", path="data/candlestick"):
    watchlist_path = os.path.join(path, watchlist)
    with open(watchlist_path) as f:
        stock_codes = [line.strip() for line in f.readlines()]

    data_path = os.path.join(path, market)

    signals = list()
    for stock_code in stock_codes:
        stock_path = os.path.join(data_path, stock_code)
        filenames = os.listdir(stock_path)
        if not filenames:
            continue
        stock_price = os.path.join(stock_path, [filename for filename in filenames if re.match(
            r"hist_price_\d{8}_\d{8}.csv", filename)][0])

        stock_df = pd.read_csv(stock_price)

        his_candlesticks = stock_df.iloc[-params["his_size"] - 1:].to_dict(orient="records")
        cur_candlestick = stock_df.iloc[-1].to_dict()

        if is_hammer_signal(cur_candlestick, his_candlesticks,
                            abs_slope=params["abs_slope"],
                            t1=params["t1"],
                            t3=params["t3"],
                            small_body=params["small_body"],
                            enhanced=params["enhanced"]):
            print("A signal is found for {stock} on {day}".format(stock=stock_code, day=stock_df.iloc[-1]["date"]))
            signals.append({"date": stock_df.iloc[-1]["date"], "stock_code": stock_code})
        # else:
        #     print("{stock} has been scanned.".format(stock=stock_code))

    filename = os.path.join(path, "hammer_signal_{market}_{date}.csv".
                            format(market=market, date=datetime.today().strftime("%Y%m%d")))
    pd.DataFrame(signals).to_csv(filename, index=False, header=True)

    return signals


if __name__ == "__main__":
    get_data(watchlist="hs_watchlist", market="hs_stock", last_days=21, path="data/candlestick")

    hs_params_dict = {
        "his_size": 5,
        "fut_size": 2,
        "abs_slope": 0.05,
        "t1": 1,
        "t3": 2,
        "small_body": 0.1,
        "enhanced": True,
    }
    scan_daily_hammer_signal(hs_params_dict, watchlist="hs_watchlist", market="hs_stock")

    get_data(watchlist="asx_watchlist", market="asx_stock", last_days=21, path="data/candlestick")

    asx_params_dict = {
        "his_size": 5,
        "fut_size": 2,
        "abs_slope": 0.01,
        "t1": 1,
        "t3": 2,
        "small_body": 0.1,
        "enhanced": True,
    }
    scan_daily_hammer_signal(asx_params_dict, watchlist="asx_watchlist", market="asx_stock")
