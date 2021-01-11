"""
    1) moderately bullish in past 12 months (53 weeks * 5 trading days)
    2) moderately bullish in past 12 weeks (12 weeks * 5 trading days)
    3) break lower bollinger band (low price)
    4) rsi <= 35
    5) hammer/inverted_hammer candlestick

    (1 or 2) and (3 or 4) and 5
"""
from datetime import date

import numpy as np
import pandas as pd
# noinspection PyUnresolvedReferences
import pandas_ta as ta
from dateutil.relativedelta import relativedelta

from ta_candlestick.pattern import is_hammer, is_inverted_hammer
from ta_indicator.trend import is_upward_or_downward_trend
from ta_stock_market_data.yahoo import get_stock_market_data, stock_data_dfs_read_csv

relative_days = 366


def exec_s01(df, exec_date):
    df0 = df[df.date <= exec_date]

    # Validate whether df has sufficient data.
    # At least S01 requires 60 trading days' data.
    if df0.iloc[-1]["date"] != exec_date:
        raise ValueError("The stock data is inconsistent with the given exec_date.")

    if len(df0) < 60:
        return False

    # condition 1: moderately bullish in past 12 months (53 * 5 = 265 trading days)
    if len(df0) > 265:
        df1 = df0.iloc[-265:]
    else:
        df1 = df0

    candlesticks = df1.to_dict(orient="records")
    close_prices = [candlestick['close'] for candlestick in candlesticks if not np.isnan(candlestick['close'])]
    _, degree = is_upward_or_downward_trend(close_prices)
    if 0 <= degree <= 45:
        cond1 = True
    else:
        cond1 = False

    # condition 2: moderately bullish in past 3 months (12 * 5 = 60 trading days)
    df2 = df0.iloc[-60:]

    candlesticks = df2.to_dict(orient="records")
    close_prices = [candlestick['close'] for candlestick in candlesticks if not np.isnan(candlestick['close'])]
    _, degree = is_upward_or_downward_trend(close_prices)
    if 0 <= degree <= 45:
        cond2 = True
    else:
        cond2 = False

    # condition 3: break lower bollinger band (low price)
    df3 = df1

    bbs = df3.ta.bbands(length=20, std=2)
    today_bbl = bbs.iloc[-1].to_list()[0]
    today_low = df.iloc[-1]["low"]
    if today_low <= today_bbl:
        cond3 = True
    else:
        cond3 = False

    # condition 4: rsi <= 35
    df4 = df1

    rsi = df4.ta.rsi(length=14)
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
        if exec_s01(df, today):
            print(stock_code)
            today = df.iloc[-1]["date"]
            strategy_no = "s01"
            results.append({"date": today, "strategy": strategy_no, "stock_code": stock_code})

    return results


if __name__ == "__main__":
    s01_stock_market_data_path = get_stock_market_data(watchlist="data/stock_codes/asx_200_stock_codes",
                                                       relative_days=relative_days,
                                                       data_types=["price"])
    s01_results = exec_strategy(watchlist="data/stock_codes/asx_200_stock_codes",
                                stock_market_data_path=s01_stock_market_data_path)

    pd.DataFrame(s01_results).to_csv("data/results/strategy_{no}_{today}.csv".format(
        no="s01",
        today=date.today().strftime("%Y%m%d")),
        index=False,
        header=True)
