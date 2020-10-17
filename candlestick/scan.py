"""
    Scan candlestick patterns.
"""

import os
from datetime import datetime, timedelta

import pandas as pd

from candlestick.core.signal import is_hammer_signal
from stock_market_data.yahoo import get_stock_historical_data, export_stock_info_df_to_csv


def get_data(last_days=21, watchlist="data/candlestick/hs_watchlist", stock_path="data/candlestick/stock"):
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
                                        end_date=end_date,
                                        full_csv_filename=False)

        export_stock_info_df_to_csv(dfs, path=stock_path)


def scan_daily_hammer_signal(params, watchlist="data/candlestick/hs_watchlist", stock_path="data/candlestick/stock"):
    with open(watchlist) as f:
        stock_codes = [line.strip() for line in f.readlines()]

    signals = list()
    for stock_code in stock_codes:
        code, market = stock_code.split(".")
        # short_csv_filename.
        name = "{market}_{code}_{date_type}.csv".format(
            market=market,
            code=code,
            date_type="price")

        price_df = pd.read_csv(os.path.join(stock_path, name))

        # By default, it scans the last candlestick in the price_df.
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

    return signals


if __name__ == "__main__":
    # get_data(watchlist="data/candlestick/hs_watchlist", last_days=14, stock_path="data/candlestick/stock")

    # hs_params_dict = {
    #     "his_size": 5,
    #     "fut_size": 2,
    #     "abs_slope": 0.05,
    #     "t1": 1,
    #     "t3": 2,
    #     "small_body": 0.1,
    #     "enhanced": True,
    # }
    # hs_signals = scan_daily_hammer_signal(params=hs_params_dict,
    #                                       watchlist="data/candlestick/hs_watchlist",
    #                                       stock_path="data/candlestick/stock")
    #
    # pd.DataFrame(hs_signals).to_csv("data/candlestick/results/hammer_signal_hs_stock_20201017",
    #                                 index=False,
    #                                 header=True)

    # get_data(watchlist="data/candlestick/asx_watchlist", last_days=14, stock_path="data/candlestick/stock")

    asx_params_dict = {
        "his_size": 5,
        "fut_size": 2,
        "abs_slope": 0.01,
        "t1": 1,
        "t3": 2,
        "small_body": 0.1,
        "enhanced": True,
    }

    asx_signals = scan_daily_hammer_signal(params=asx_params_dict,
                                           watchlist="data/candlestick/asx_watchlist",
                                           stock_path="data/candlestick/stock")

    # pd.DataFrame(asx_signals).to_csv("data/candlestick/results/hammer_signal_asx_stock_{today}}".format(
    #     today=datetime.today().strftime("")
    # ),
    #                                  index=False,
    #                                  header=True)
