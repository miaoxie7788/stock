"""
    1) moderately bullish in past 12 months
    2) moderately bullish in past 3 months (12 weeks)
    3) break lower bollinger band
    4) rsi <= 35
    5) hammer/inverted_hammer candlestick
"""

import os
from datetime import datetime

import numpy as np
import pandas as pd
# noinspection PyUnresolvedReferences
import pandas_ta as ta
from dateutil.relativedelta import relativedelta

from ta_candlestick.pattern import is_hammer, is_inverted_hammer
from ta_indicator.trend import is_upward_or_downward_trend
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

    m12_stock_path = os.path.join(path, "{market}_12m".format(market=market))
    w12_stock_path = os.path.join(path, "{market}_12w".format(market=market))
    d42_stock_path = os.path.join(path, "{market}_42d".format(market=market))

    # Read watchlist.
    with open(watchlist) as f:
        stock_codes = [line.strip() for line in f.readlines()]

    today = datetime.today()

    # Get historical price data for stocks.
    for stock_code in stock_codes:
        # 12 months data
        month_dfs = get_stock_historical_data(stock_code=stock_code,
                                              data_types=["price"],
                                              start_date=today - relativedelta(months=12),
                                              end_date=today,
                                              interval="1mo")

        export_stock_info_df_to_csv(month_dfs, path=m12_stock_path)

        # 3 months (12 weeks) data
        week_dfs = get_stock_historical_data(stock_code=stock_code,
                                             data_types=["price"],
                                             start_date=today - relativedelta(weeks=12),
                                             end_date=today,
                                             interval="1wk")

        export_stock_info_df_to_csv(week_dfs, path=w12_stock_path)

        # 6 week (42 days) data
        day_dfs = get_stock_historical_data(stock_code=stock_code,
                                            data_types=["price"],
                                            start_date=today - relativedelta(days=42),
                                            end_date=today,
                                            interval="1d")

        export_stock_info_df_to_csv(day_dfs, path=d42_stock_path)


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

    m12_stock_path = os.path.join(path, "{market}_12m".format(market=market))
    w12_stock_path = os.path.join(path, "{market}_12w".format(market=market))
    d42_stock_path = os.path.join(path, "{market}_42d".format(market=market))

    with open(watchlist) as f:
        stock_codes = [line.strip() for line in f.readlines()]

    results = list()
    for stock_code in stock_codes:
        # condition 1: moderately bullish in past 12 months
        df = stock_market_data_read_csv(stock_code, m12_stock_path)
        if df is None:
            print("{stock} does not have data.".format(stock=stock_code))
            continue

        if len(df) > 12:
            df = df.iloc[-12:]

        candlesticks = df.to_dict(orient="records")

        close_prices = [candlestick['close'] for candlestick in candlesticks if not np.isnan(candlestick['close'])]
        _, degree = is_upward_or_downward_trend(close_prices)
        if 0 <= degree <= 45:
            cond1 = True
        else:
            cond1 = False

        # condition 2: moderately bullish in past 3 months (12 weeks)
        df = stock_market_data_read_csv(stock_code, w12_stock_path)
        if df is None:
            print("{stock} does not have data.".format(stock=stock_code))
            continue

        if len(df) > 12:
            df = df.iloc[-12:]

        candlesticks = df.to_dict(orient="records")
        close_prices = [candlestick['close'] for candlestick in candlesticks if not np.isnan(candlestick['close'])]
        _, degree = is_upward_or_downward_trend(close_prices)
        if 0 <= degree <= 45:
            cond2 = True
        else:
            cond2 = False

        # condition 3: break lower bollinger band
        df = stock_market_data_read_csv(stock_code, d42_stock_path)

        bbs = df.ta.bbands(length=20, std=2)
        today_bbl = bbs.iloc[-1].to_list()[0]
        today_close = df.iloc[-1]["close"]
        if today_close <= today_bbl:
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

        if (cond1 and cond2) and (cond3 or cond4) and cond5:
            print(stock_code)
            today = df.iloc[-1]["date"]
            strategy_no = "s01"
            results.append({"date": today, "strategy": strategy_no, "stock_code": stock_code})

    return results


if __name__ == "__main__":
    # get_data(watchlist="data/stock_codes/asx_200_stock_codes")
    s01_results = exec_strategy(watchlist="data/stock_codes/asx_200_stock_codes")

    pd.DataFrame(s01_results).to_csv("data/results/strategy_{no}_{today}.csv".format(
        no="s01",
        today=datetime.today().strftime("%Y%m%d")),
        index=False,
        header=True)
