"""
    1) moderately bullish in past 12 months
    2) moderately bullish in past 3 months (12 weeks)
    3) break lower bollinger band
    4) rsi <= 35
    5) hammer/reverse_hammer candlestick
    6) declining volume trend
"""

import os
from datetime import datetime

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta

from ta_candlestick.core.trend import is_bullish_or_bearish_trend
from ta_stock_market_data.yahoo import get_stock_historical_data, export_stock_info_df_to_csv


def get_data(watchlist, path="data"):
    """
        Get historical price data for stocks presented in the watchlist.
    """

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

        export_stock_info_df_to_csv(month_dfs, path=os.path.join(path, "stock_12m"))

        # 3 months (12 weeks) data
        week_dfs = get_stock_historical_data(stock_code=stock_code,
                                             data_types=["price"],
                                             start_date=today - relativedelta(weeks=12),
                                             end_date=today,
                                             interval="1wk")

        export_stock_info_df_to_csv(week_dfs, path=os.path.join(path, "stock_12w"))

        # 3 week (21 days) data
        day_dfs = get_stock_historical_data(stock_code=stock_code,
                                            data_types=["price"],
                                            start_date=today - relativedelta(days=21),
                                            end_date=today,
                                            interval="1d")

        export_stock_info_df_to_csv(day_dfs, path=os.path.join(path, "stock_21d"))


def is_break_bollinger_bands(candlesticks, key="close"):
    prices = [candlestick[key] for candlestick in candlesticks[:-1]]

    last_price = candlesticks[-1][key]

    if last_price < np.mean(prices) - 2 * np.std(prices):
        return True

    return False


def exec_strategy(watchlist, path="data"):
    with open(watchlist) as f:
        stock_codes = [line.strip() for line in f.readlines()]

    stock_path_1m = os.path.join(path, "stock_1m")
    stock_path_1w = os.path.join(path, "stock_1w")
    stock_path_1d = os.path.join(path, "stock_1d")

    for stock_code in stock_codes:
        code, market = stock_code.split(".")
        # short_csv_filename.
        name = "{market}_{code}_{date_type}.csv".format(
            market=market,
            code=code,
            date_type="price")

        both_bullish = 0

        for stock_path in [stock_path_1m, stock_path_1w]:
            filename = os.path.join(stock_path, name)
            if os.path.exists(filename):
                price_df = pd.read_csv(filename)
            else:
                # print("{stock} does not have data.".format(stock=stock_code))
                continue

            candlesticks = price_df.iloc[-12:].to_dict(orient="records")
            _, degree = is_bullish_or_bearish_trend(candlesticks)
            if 0 <= degree <= 45:
                both_bullish += 1

        filename = os.path.join(stock_path_1d, name)
        if os.path.exists(filename):
            price_df = pd.read_csv(filename)
        else:
            # print("{stock} does not have data.".format(stock=stock_code))
            continue

        candlesticks = price_df.to_dict(orient="records")

        break_bollinger = 0
        if is_break_bollinger_bands(candlesticks):
            break_bollinger = 1

        if break_bollinger == 1 and both_bullish == 2:
            print(stock_code)


if __name__ == "__main__":
    get_data(watchlist="data/stock_codes/stock_code_list_asx_200")
    # exec_strategy(watchlist="data/stock_codes/stock_code_list_asx_200")
