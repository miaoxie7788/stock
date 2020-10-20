"""
    Scan candlestick patterns.
"""

import os
from datetime import datetime, timedelta

import pandas as pd

from candlestick.core.pattern import is_bullish_hammer
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


def scan_bullish_hammer(price_df, params):
    """
        params = {
            "bullish_hammer_params": {
                "hammer_params": {"t1": 1,
                                  "t3": 2,
                                  "small_body": 0.05},
                "key": "low",
                "abs_slope": 0.25,
                "enhanced": True,
            },
            "ref_size": 5,
            }
    """
    scan_date = price_df.iloc[-1]["date"]
    stock_code = price_df.iloc[-1]["ticker"]
    ref_size = params["ref_size"]
    candlestick = price_df.iloc[-1].to_dict()

    pattern = None
    if len(price_df) - 1 < ref_size:
        print("{stock_code} does not have {ref_size} ref candlesticks".format(ref_size=ref_size, stock_code=stock_code))
    else:
        ref_candlesticks = price_df.iloc[-ref_size - 1:-1].to_dict(orient="records")

        if is_bullish_hammer(candlestick, ref_candlesticks, params["bullish_hammer_params"]):
            print("A bullish hammer is found for {stock} on {day}".format(stock=stock_code, day=scan_date))
            pattern = {"date": scan_date, "stock_code": stock_code, "pattern": "bullish_hammer"}

    return pattern


def scan_patterns(params, watchlist="data/candlestick/hs_watchlist", stock_path="data/candlestick/stock"):
    with open(watchlist) as f:
        stock_codes = [line.strip() for line in f.readlines()]

    patterns = list()
    for stock_code in stock_codes:
        code, market = stock_code.split(".")
        # short_csv_filename.
        name = "{market}_{code}_{date_type}.csv".format(
            market=market,
            code=code,
            date_type="price")

        filename = os.path.join(stock_path, name)
        if os.path.exists(filename):
            price_df = pd.read_csv(filename)
        else:
            print("{stock} does not have data.".format(stock=stock_code))
            continue

        pattern = scan_bullish_hammer(price_df, params)
        if pattern:
            patterns.append(pattern)

    return patterns


if __name__ == "__main__":
    get_data(watchlist="data/candlestick/hs_watchlist", last_days=14, stock_path="data/candlestick/stock")

    hs_params = {
        "bullish_hammer_params": {
            "hammer_params": {"t1": 3,
                              "t3": 4,
                              "small_body": 0.05},
            "key": "low",
            "abs_slope": 0.25,
            "enhanced": True,
        },
        "ref_size": 5,
    }

    hs_patterns = scan_patterns(params=hs_params,
                                watchlist="data/candlestick/hs_watchlist",
                                stock_path="data/candlestick/stock")

    pd.DataFrame(hs_patterns).to_csv("data/candlestick/results/hs_stock_patterns_{today}.csv".format(
        today=datetime.today().strftime("%Y%m%d")),
        index=False,
        header=True)

    get_data(watchlist="data/candlestick/asx_watchlist", last_days=14, stock_path="data/candlestick/stock")

    asx_params = {
        "bullish_hammer_params": {
            "hammer_params": {"t1": 1,
                              "t3": 2,
                              "small_body": 0.1},
            "key": "low",
            "abs_slope": 0.02,
            "enhanced": True,
        },
        "ref_size": 5,
    }
    asx_patterns = scan_patterns(params=asx_params,
                                 watchlist="data/candlestick/asx_watchlist",
                                 stock_path="data/candlestick/stock")

    pd.DataFrame(asx_patterns).to_csv("data/candlestick/results/asx_stock_patterns_{today}.csv".format(
        today=datetime.today().strftime("%Y%m%d")),
        index=False,
        header=True)
