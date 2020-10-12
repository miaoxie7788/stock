"""
    Scan candlestick patterns.
"""

import os
import re
from datetime import datetime, timedelta

import pandas as pd

from candlestick.core.signal import is_hammer_signal
from stock_market_data.yahoo import get_stock_historical_data


def scan_daily_hammer_signal():
    path = "data/candlestick"

    # Read watchlist.
    watchlist_path = os.path.join(path, "hs_watchlist")
    with open(watchlist_path) as f:
        hs_stocks = [stock.strip() for stock in f.readlines()]

    data_path = os.path.join(path, "hs_stock")
    if not os.path.exists(data_path):
        os.mkdir(data_path)

    # Get stock historical data between start_date and end_date, which should be longer than the window size (i.e., 5).
    today = datetime.today()
    start_date = today - timedelta(days=21)
    end_date = today

    for stock_code in hs_stocks:
        get_stock_historical_data(stock_code=stock_code, start_date=start_date, end_date=end_date, path=data_path)

    # Apply scan_hammer to scan signals.

    params_dict = {
        "his_size": 5,
        "fut_size": 2,
        "abs_slope": 0.05,
        "t1": 1,
        "t3": 2,
        "small_body": 0.1,
        "enhanced": True,
    }

    signals = list()
    for stock_code in hs_stocks:
        stock_path = os.path.join(data_path, stock_code)
        stock_price = os.path.join(stock_path, [filename for filename in os.listdir(stock_path) if re.match(
            r"hist_price_\d{8}_\d{8}.csv", filename)][0])

        stock_df = pd.read_csv(stock_price)

        his_candlesticks = stock_df.iloc[-params_dict["his_size"] - 1:].to_dict(orient="records")
        cur_candlestick = stock_df.iloc[-1].to_dict()

        if is_hammer_signal(cur_candlestick, his_candlesticks,
                            abs_slope=params_dict["abs_slope"],
                            t1=params_dict["t1"],
                            t3=params_dict["t3"],
                            small_body=params_dict["small_body"],
                            enhanced=params_dict["enhanced"]):
            print("A signal is found for {stock} on {day}".format(stock=stock_code, day=stock_df.iloc[-1]["date"]))
            signals.append({"date": stock_df.iloc[-1]["date"], "stock_code": stock_code})
        else:
            print("{stock} has been scanned.".format(stock=stock_code))

    return signals


if __name__ == "__main__":
    df = scan_daily_hammer_signal()
    pd.DataFrame(df).to_csv("hammer_signals_20201012.csv", index=False, header=True)
