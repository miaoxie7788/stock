"""
    1) bearish in past 1 week
    2) hammer/inverted_hammer candlestick
    3) close higher than open
    4) volume presented in a declining trend
"""

import os
from datetime import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta

from ta_candlestick.pattern import is_bullish_or_bearish_candlestick, is_hammer, is_inverted_hammer
from ta_indicator.trend import is_bullish_or_bearish_trend
from ta_stock_market_data.yahoo import get_stock_historical_data, export_stock_info_df_to_csv


def get_data(watchlist, path="data"):
    """
        Get historical price data for stocks presented in the watchlist.
    """

    # stock market: asx or hs
    if "asx" in watchlist:
        market = "asx"
    elif "hs" in watchlist:
        market = "hs"
    else:
        market = ""

    d14_stock_path = os.path.join(path, "{market}_14d".format(market=market))

    # Read watchlist.
    with open(watchlist) as f:
        stock_codes = [line.strip() for line in f.readlines()]

    today = datetime.today()

    # Get historical price data for stocks.
    for stock_code in stock_codes:
        # 2 week (14 days) data
        day_dfs = get_stock_historical_data(stock_code=stock_code,
                                            data_types=["price"],
                                            start_date=today - relativedelta(days=14),
                                            end_date=today,
                                            interval="1d")

        export_stock_info_df_to_csv(day_dfs, path=d14_stock_path)


def stock_market_data_read_csv(stock_code, path, data_type="price"):
    code, market = stock_code.split(".")
    # short_csv_filename.
    csv_filename = "{market}_{code}_{date_type}.csv".format(
        market=market,
        code=code,
        date_type=data_type)

    stock_path = os.path.join(path, csv_filename)
    try:
        df = pd.read_csv(stock_path)
    except FileNotFoundError:
        df = None

    return df


def exec_strategy(watchlist, path="data"):
    # stock market: asx or hs
    if "asx" in watchlist:
        market = "asx"
    elif "hs" in watchlist:
        market = "hs"
    else:
        market = ""

    d14_stock_path = os.path.join(path, "{market}_14d".format(market=market))

    with open(watchlist) as f:
        stock_codes = [line.strip() for line in f.readlines()]

    results = list()
    for stock_code in stock_codes:
        # condition 1: bearish in past 1 week.
        df = stock_market_data_read_csv(stock_code, d14_stock_path)
        if df is None:
            print("{stock} does not have data.".format(stock=stock_code))
            continue

        if len(df) > 7:
            df = df.iloc[-7:]

        candlesticks = df.to_dict(orient="records")
        _, degree = is_bullish_or_bearish_trend(candlesticks, key="close")
        if degree < 0:
            cond1 = True
        else:
            cond1 = False

        # condition 2: hammer/inverted_hammer candlestick
        today_candlestick = df.iloc[-1]

        if is_hammer(today_candlestick, 1, 2, 0.1) or is_inverted_hammer(today_candlestick, 2, 1, 0.1):
            cond2 = True
        else:
            cond2 = False

        # condition 3: close higher than open
        if is_bullish_or_bearish_candlestick(today_candlestick) == "bullish":
            cond3 = True
        else:
            cond3 = False

        # condition 4: volume presented in a declining trend
        _, degree = is_bullish_or_bearish_trend(candlesticks, key="volume")
        if degree < 0:
            cond4 = True
        else:
            cond4 = False

        if cond1 and cond2 and cond3 and cond4:
            print(stock_code)
            today = df.iloc[-1]["date"]
            strategy_no = "s01"
            results.append({"date": today, "strategy": strategy_no, "stock_code": stock_code})

    return results


if __name__ == "__main__":
    # get_data(watchlist="data/stock_codes/asx_200_stock_codes")
    s02_results = exec_strategy(watchlist="data/stock_codes/asx_200_stock_codes")

    pd.DataFrame(s02_results).to_csv("data/results/strategy_{no}_{today}.csv".format(
        no="s02",
        today=datetime.today().strftime("%Y%m%d")),
        index=False,
        header=True)
