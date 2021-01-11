"""
    1) bearish in past 1 week
    2) hammer/inverted_hammer candlestick
    3) close higher than open
    4) volume presented in a declining trend
"""

from datetime import date

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta

from ta_candlestick.pattern import is_bullish_or_bearish_candlestick, is_hammer, is_inverted_hammer
from ta_indicator.trend import is_upward_or_downward_trend
from ta_stock_market_data.yahoo import get_stock_market_data, stock_data_dfs_read_csv

relative_days = 14


def exec_s02(df, exec_date):
    df0 = df[df.date <= exec_date]

    # Validate whether df has sufficient data.
    # At least S02 requires 7 trading days' data.
    if df0.iloc[-1]["date"] != exec_date:
        raise ValueError("The stock data is inconsistent with the given exec_date.")

    if len(df0) < 7:
        return False

    # condition 1: bearish in past 1 week.
    if len(df0) > 7:
        df1 = df0.iloc[-7:]
    else:
        df1 = df0

    candlesticks = df1.to_dict(orient="records")
    close_prices = [candlestick['close'] for candlestick in candlesticks if not np.isnan(candlestick['close'])]
    _, degree = is_upward_or_downward_trend(close_prices)
    if degree < 0:
        cond1 = True
    else:
        cond1 = False

    # condition 2: hammer/inverted_hammer candlestick
    exec_date_candlestick = df0.iloc[-1]

    if is_hammer(exec_date_candlestick, 1, 2, 0.1) or is_inverted_hammer(exec_date_candlestick, 2, 1, 0.1):
        cond2 = True
    else:
        cond2 = False

    # condition 3: close higher than open
    if is_bullish_or_bearish_candlestick(exec_date_candlestick) == "bullish":
        cond3 = True
    else:
        cond3 = False

    # condition 4: volume presented in a declining trend
    df4 = df1

    candlesticks = df4.to_dict(orient="records")
    volumes = [candlestick['volume'] for candlestick in candlesticks if not np.isnan(candlestick['volume'])]
    is_upward_or_downward, _ = is_upward_or_downward_trend(volumes)
    if is_upward_or_downward == "downward":
        cond4 = True
    else:
        cond4 = False

    if cond1 and cond2 and cond3 and cond4:
        return True

    return False


def exec_strategy(watchlist, stock_market_data_path):
    with open(watchlist) as f:
        stock_codes = [line.strip() for line in f.readlines()]

    results = list()
    for stock_code in stock_codes:
        dfs = stock_data_dfs_read_csv(stock_code, stock_market_data_path)

        if "price" not in dfs:
            print("{stock} does not have price data.".format(stock=stock_code))
            continue
        else:
            df = dfs["price"]

        today = str(date.today() - relativedelta(days=1))
        if exec_s02(df, today):
            print(stock_code)
            today = df.iloc[-1]["date"]
            strategy_no = "s02"
            results.append({"date": today, "strategy": strategy_no, "stock_code": stock_code})

    return results


if __name__ == "__main__":
    s02_stock_market_data_path = get_stock_market_data(watchlist="data/stock_codes/asx_200_stock_codes",
                                                       relative_days=relative_days,
                                                       data_types=["price"])

    s02_results = exec_strategy(watchlist="data/stock_codes/asx_200_stock_codes",
                                stock_market_data_path=s02_stock_market_data_path)

    pd.DataFrame(s02_results).to_csv("data/results/strategy_{no}_{today}.csv".format(
        no="s02",
        today=date.today().strftime("%Y%m%d")),
        index=False,
        header=True)
