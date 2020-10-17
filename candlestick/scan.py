"""
    Scan candlestick patterns.
"""

import os
import re
from datetime import datetime, timedelta

import pandas as pd

from candlestick.core.signal import is_hammer_signal
from stock_market_data.yahoo import get_stock_historical_data, export_stock_info_df_to_csv


def get_data(watchlist="data/candlestick/hs_watchlist", last_days=21, path="data/candlestick/stock"):
    """
        Get historical data for stocks presented in the watchlist between today and today-last_days.
        Note, last_days should be larger than his_size.
    """

    # Read watchlist.
    with open(watchlist) as f:
        stock_codes = [line.strip() for line in f.readlines()]

    today = datetime.today()
    start_date = today - timedelta(days=last_days)
    end_date = today + timedelta(days=1)

    for stock_code in stock_codes:
        dfs = get_stock_historical_data(stock_code=stock_code,
                                        data_types=["price"],
                                        start_date=start_date,
                                        end_date=end_date)

        export_stock_info_df_to_csv(dfs, path=path)


def scan_daily_hammer_signal(params, watchlist="hs_stock_codes", path="data/candlestick/stock"):
    with open(watchlist) as f:
        stock_codes = [line.strip() for line in f.readlines()]

    signals = list()
    for stock_code in stock_codes:
        code, market = stock_code.split(".")
        filename_regex = "{market}_{code}_{date_type}_{start_date}_{end_date}.csv".format(
            market=market,
            code=code,
            date_type="price",
            start_date=r"\d{8}",
            end_date=r"\d{8}")

        filenames = os.listdir(path)
        price_filename = os.path.join(path,
                                      [filename for filename in filenames if re.match(filename_regex, filename)][0])

        price_df = pd.read_csv(price_filename)

        his_candlesticks = price_df.iloc[-params["his_size"] - 1:].to_dict(orient="records")
        cur_candlestick = price_df.iloc[-1].to_dict()

        if is_hammer_signal(cur_candlestick, his_candlesticks,
                            abs_slope=params["abs_slope"],
                            t1=params["t1"],
                            t3=params["t3"],
                            small_body=params["small_body"],
                            enhanced=params["enhanced"]):
            print("A signal is found for {stock} on {day}".format(stock=stock_code, day=price_df.iloc[-1]["date"]))
            signals.append({"date": price_df.iloc[-1]["date"], "stock_code": stock_code})
        # else:
        #     print("{stock} has been scanned.".format(stock=stock_code))

    filename = os.path.join(path, "hammer_signal_{market}_{date}.csv".
                            format(market=market, date=datetime.today().strftime("%Y%m%d")))
    pd.DataFrame(signals).to_csv(filename, index=False, header=True)

    return signals


if __name__ == "__main__":
    # get_data(watchlist="data/candlestick/hs_watchlist", last_days=14, path="data/candlestick/stock")

    hs_params_dict = {
        "his_size": 5,
        "fut_size": 2,
        "abs_slope": 0.05,
        "t1": 1,
        "t3": 2,
        "small_body": 0.1,
        "enhanced": True,
    }
    scan_daily_hammer_signal(hs_params_dict, watchlist="data/candlestick/hs_watchlist", path="data/candlestick/stock")

    # get_data(watchlist="data/candlestick/asx_watchlist", last_days=14, path="data/candlestick/stock")
    #
    # asx_params_dict = {
    #     "his_size": 5,
    #     "fut_size": 2,
    #     "abs_slope": 0.01,
    #     "t1": 1,
    #     "t3": 2,
    #     "small_body": 0.1,
    #     "enhanced": True,
    # }
    #
    # scan_daily_hammer_signal(asx_params_dict, watchlist="data/candlestick/asx_watchlist", path="data/candlestick/stock")
