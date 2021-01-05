"""
    1) moderately bullish in past 12 months (53 weeks * 5 trading days)
    2) moderately bullish in past 12 weeks (12 weeks * 5 trading days)
    3) break lower bollinger band (low price)
    4) rsi <= 35
    5) hammer/inverted_hammer candlestick

    (1 or 2) and (3 or 4) and 5
"""

import os
from datetime import date

import numpy as np
import pandas as pd
# noinspection PyUnresolvedReferences
import pandas_ta as ta
from dateutil.relativedelta import relativedelta

from ta_candlestick.pattern import is_hammer, is_inverted_hammer
from ta_indicator.trend import is_upward_or_downward_trend
from ta_stock_market_data.yahoo import get_stock_historical_data, export_stock_info_df_to_csv

DAYS366 = 366


def get_stock_market_data(watchlist, path="data"):
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

    # Read watchlist.
    with open(watchlist) as f:
        stock_codes = [line.strip() for line in f.readlines()]

    today = date.today()

    # Get historical price data for stocks.
    for stock_code in stock_codes:
        # 1 year (366 days) data
        start_date = today - relativedelta(days=DAYS366)
        day_dfs = get_stock_historical_data(stock_code=stock_code,
                                            data_types=["price"],
                                            start_date=start_date,
                                            end_date=today,
                                            interval="1d")

        stock_market_data_path = os.path.join(path, "{market}_{start_date}_{today}".format(
            market=market,
            start_date=str(start_date).replace("-", ""),
            today=str(today).replace("-", "")))
        export_stock_info_df_to_csv(day_dfs, path=stock_market_data_path)


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

    today = date.today()
    start_date = today - relativedelta(days=DAYS366)
    stock_market_data_path = os.path.join(path, "{market}_{start_date}_{today}".format(
        market=market,
        start_date=str(start_date).replace("-", ""),
        today=str(today).replace("-", "")))

    with open(watchlist) as f:
        stock_codes = [line.strip() for line in f.readlines()]

    results = list()
    for stock_code in stock_codes:
        df = stock_market_data_read_csv(stock_code, stock_market_data_path)
        if df is None:
            print("{stock} does not have data.".format(stock=stock_code))
            continue

        # condition 1: moderately bullish in past 12 months (53 * 5 = 265 trading days)
        if len(df) > 265:
            m12_df = df.iloc[-265:]
        else:
            m12_df = df

        candlesticks = m12_df.to_dict(orient="records")
        close_prices = [candlestick['close'] for candlestick in candlesticks if not np.isnan(candlestick['close'])]
        _, degree = is_upward_or_downward_trend(close_prices)
        if 0 <= degree <= 45:
            cond1 = True
        else:
            cond1 = False

        # condition 2: moderately bullish in past 3 months (12 * 5 = 60 trading days)
        if len(df) > 60:
            w12_df = df.iloc[-60:]
        else:
            w12_df = df

        candlesticks = w12_df.to_dict(orient="records")
        close_prices = [candlestick['close'] for candlestick in candlesticks if not np.isnan(candlestick['close'])]
        _, degree = is_upward_or_downward_trend(close_prices)
        if 0 <= degree <= 45:
            cond2 = True
        else:
            cond2 = False

        # condition 3: break lower bollinger band (low price)
        bbs = df.ta.bbands(length=20, std=2)
        today_bbl = bbs.iloc[-1].to_list()[0]
        today_low = df.iloc[-1]["low"]
        if today_low <= today_bbl:
            cond3 = True
        else:
            cond3 = False

        # condition 4: rsi <= 35
        rsi = df.ta.rsi(length=14)
        today_rsi = rsi.iloc[-1]
        if today_rsi <= 35:
            cond4 = True
        else:
            cond4 = False

        # condition 5: hammer/inverted_hammer candlestick
        today_candlestick = df.iloc[-1]

        if is_hammer(today_candlestick, 1, 2, 0.1) or is_inverted_hammer(today_candlestick, 2, 1, 0.1):
            cond5 = True
        else:
            cond5 = False

        if (cond1 or cond2) and (cond3 or cond4) and cond5:
            print(stock_code)
            today = df.iloc[-1]["date"]
            strategy_no = "s01"
            results.append({"date": today, "strategy": strategy_no, "stock_code": stock_code})

    return results


if __name__ == "__main__":
    # get_stock_market_data(watchlist="data/stock_codes/asx_200_stock_codes")
    s01_results = exec_strategy(watchlist="data/stock_codes/asx_200_stock_codes")

    pd.DataFrame(s01_results).to_csv("data/results/strategy_{no}_{today}.csv".format(
        no="s01",
        today=date.today().strftime("%Y%m%d")),
        index=False,
        header=True)
