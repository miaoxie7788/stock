import os
import re

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from candlestick.core.pattern import is_bullish_hammer, is_bullish_inverted_hammer


def plot_candlestick(price_df):
    fig = go.Figure(data=[go.Candlestick(
        x=price_df['date'],
        open=price_df['open'],
        high=price_df['high'],
        low=price_df['low'],
        close=price_df['close'])])

    fig.show()


def debug(window_df):
    while True:
        date = input("Type the date to plot its neighbouring candlesticks: \n")
        window = window_df.loc[window_df["date"] == date]

        candlesticks = [*window['his'].values[0], window['cur'].values[0], *window['fut'].values[0]]
        plot_candlestick(pd.DataFrame(candlesticks))


def evaluate_any_higher_price1(windows, key="close", a_share=False):
    """"
        Each window is a dict of date, his_candlesticks, cur_candlestick, fut_candlesticks.

        E.g., his_size = 3, fut_size = 2, cur_candlestick = c0
        c-3, c-2, c-1, c0, c1, c2

        It evaluates if there is any price of [c1, c2] (by default close price) higher than price of c0. If yes,
        it indicates "success"; otherwise "failure".
    """

    def any_higher_price(row):

        # HS stock is T+1.
        if a_share:
            fut_candlesticks = row["fut"][1:]
            cut_price = row["cur"][key]
        # ASX stock is T+0.
        else:
            fut_candlesticks = row["fut"]
            cut_price = row["cur"][key]

        fut_prices = [candlestick[key] for candlestick in fut_candlesticks if not np.isnan(candlestick[key])]
        if fut_prices:
            max_fut_price = max(fut_prices)
        else:
            max_fut_price = 0

        return round(max_fut_price / cut_price - 1, 3)

    windows_df = pd.DataFrame(windows)
    windows_df["higher_fut_price"] = windows_df.apply(any_higher_price, axis="columns")

    return windows_df


# params = {"date": "2020-10-10", "fut_size": 3, "key": "close", "a_share": False}
# result = {}
def evaluate_higher_price(price_df, params):
    """"
        It evaluates if there is any price of [c1, c2, ..., c_fut_size] (by default close price) higher than price of
        c0. If yes, it indicates "success"; otherwise "failure".
    """
    price_df = price_df.sort_values(by="date", axis='index', ascending=True) \
        .reset_index().drop(labels="index", axis="columns")

    date = params["date"]
    # By default, it evaluates the first candlestick in the price_df.
    if not date:
        date_index = 0
        date = price_df.iloc[date_index]["date"]
    else:
        date_index = price_df.index[price_df["date"] == date]
        if len(date_index) > 0:
            date_index = date_index[0]
        else:
            return None

    fut_size = params["fut_size"]
    stock_code = price_df.iloc[date_index]["ticker"]

    if date_index + fut_size > len(price_df):
        print("{stock_code} does not have {fut_size} future candlesticks."
              .format(fut_size=fut_size, stock_code=stock_code))
        return None

    key = params["key"]
    a_share = params["a_share"]

    price = price_df.iloc[date_index]["close"]
    if a_share:
        fut_prices = price_df.iloc[date_index + 1:date_index + fut_size - 1][key]
    else:
        fut_prices = price_df.iloc[date_index:date_index + fut_size][key]

    max_fut_price = fut_prices.max()

    result = params
    # Number of trade days that a higher price occurs.
    result["bullish_days"] = fut_prices.ge(price).sum()
    # Highest price.
    result["highest_price"] = max_fut_price
    # Highest percentage.
    result["highest_percent"] = round(max_fut_price / price - 1, 3)

    return result


def evaluate_bullish_trend(windows, key="close", print_detail=True):
    pass


def evaluate_signal_confidence(stock_code, params, eval_signal, stock_path="data/stock"):
    code, market = stock_code.split(".")
    name_regex = "{market}_{code}_{date_type}_{start_date}_{end_date}.csv".format(
        market=market,
        code=code,
        date_type="price",
        start_date=r"\d{8}",
        end_date=r"\d{8}")

    names = os.listdir(stock_path)
    filename = os.path.join(stock_path, [name for name in names if re.match(name_regex, name)][0])

    price_df = pd.read_csv(filename)

    eval_signal_func_dict = {
        "hammer": evaluate_hammer_signal,
        "inverted_hammer": evaluate_inverted_hammer_signal,
    }

    eval_signal_func = eval_signal_func_dict[eval_signal]
    windows = eval_signal_func(price_df, **params)


def evaluate_hammer_signal(price_df, params):
    """
        Evaluate how a stock performs historically against hammer_signal.
    """

    n = len(price_df)
    windows = list()
    for t in range(params["ref_size"], n - params["fut_size"]):
        ref_candlesticks = price_df.iloc[t - params["ref_size"]: t].to_dict(orient="records")
        candlestick = price_df.iloc[t].to_dict()
        fut_candlesticks = price_df.iloc[t + 1: t + params["fut_size"] + 1].to_dict(orient="records")

        if is_bullish_hammer(candlestick, ref_candlesticks, params["bullish_hammer_params"]):
            signal = True
        else:
            signal = False

        window = {"date": candlestick["date"], "cur": candlestick, "his": ref_candlesticks,
                  "fut": fut_candlesticks, "is_hammer_signal": signal}

        windows.append(window)

    # windows_df = evaluate_any_higher_price(windows, key="high", a_share=True)
    # windows_df0 = windows_df.loc[windows_df["is_hammer_signal"]]
    #
    # n = len(windows_df)
    # n0 = len(windows_df0)
    #
    # rate = len(windows_df[windows_df["higher_fut_price"] >= 0]) / n
    # if n0 == 0:
    #     rate0 = 0
    # else:
    #     rate0 = len(windows_df0[windows_df0["higher_fut_price"] >= 0]) / n0
    #
    # # scale: billion
    # trade_scale = round(price_df.apply(lambda row: row["volume"] * row["close"], axis="columns").mean() / 1000000000, 3)
    #
    # result = {
    #     "stock_code": stock_code,
    #     "trade_scale": trade_scale,
    #     "trade_days": n,
    #     "n_hammer_signal": n0,
    #     "benchmark_success_rate": round(rate, 3),
    #     "success_rate": round(rate0, 3),
    #     "improvement": round(rate0 / rate - 1, 3),
    #     "method": "any_higher_high_price",
    #     **params_dict
    # }
    return windows


def evaluate_inverted_hammer_signal(price_df, his_size, fut_size, abs_slope, t1, t3, small_body, enhanced):
    """
        Scan inverted_hammer signals in each window across the price_df.
    """
    n = len(price_df)
    windows = list()
    for t in range(his_size, n - fut_size):
        his_candlesticks = price_df.iloc[t - his_size: t].to_dict(orient="records")
        cur_candlestick = price_df.iloc[t].to_dict()
        fut_candlesticks = price_df.iloc[t + 1: t + fut_size + 1].to_dict(orient="records")

        if is_bullish_inverted_hammer(cur_candlestick, his_candlesticks, abs_slope, t1, t3, small_body, enhanced):
            signal = True
        else:
            signal = False

        window = {"date": cur_candlestick["date"], "cur": cur_candlestick, "his": his_candlesticks,
                  "fut": fut_candlesticks, "is_inverted_hammer_signal": signal}

        windows.append(window)

    return windows
