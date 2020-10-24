import pandas as pd
import plotly.graph_objects as go

from candlestick.core.pattern import is_bullish_hammer, is_bullish_inverted_hammer
from candlestick.core.trend import is_bullish_or_bearish_trend


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


# def evaluate_any_higher_price1(windows, key="close", a_share=False):
#     """"
#         Each window is a dict of date, his_candlesticks, cur_candlestick, fut_candlesticks.
#
#         E.g., his_size = 3, fut_size = 2, cur_candlestick = c0
#         c-3, c-2, c-1, c0, c1, c2
#
#         It evaluates if there is any price of [c1, c2] (by default close price) higher than price of c0. If yes,
#         it indicates "success"; otherwise "failure".
#     """
#
#     def any_higher_price(row):
#
#         # HS stock is T+1.
#         if a_share:
#             fut_candlesticks = row["fut"][1:]
#             cut_price = row["cur"][key]
#         # ASX stock is T+0.
#         else:
#             fut_candlesticks = row["fut"]
#             cut_price = row["cur"][key]
#
#         fut_prices = [candlestick[key] for candlestick in fut_candlesticks if not np.isnan(candlestick[key])]
#         if fut_prices:
#             max_fut_price = max(fut_prices)
#         else:
#             max_fut_price = 0
#
#         return round(max_fut_price / cut_price - 1, 3)
#
#     windows_df = pd.DataFrame(windows)
#     windows_df["higher_fut_price"] = windows_df.apply(any_higher_price, axis="columns")
#
#     return windows_df


def evaluate_higher_price(price_df, date_or_index, fut_size, key, a_share):
    """"
        Evaluate whether there is any higher price than the trade day, according to future fut_size trade days. Key
        can be high, low, open or close.

        {"date": "2020-10-10", "fut_size": 3, "key": "close", "a_share": False}

        # bullish_days:             number of future trade days those have a higher price.
        # highest price:            highest price occurred in future trade days.
        # highest growth:           highest growth rate.
        # bullish trend:            whether a bullish tread is present in future trade days.
    """
    price_df = price_df.sort_values(by="date", axis='index', ascending=True) \
        .reset_index().drop(labels="index", axis="columns")

    # By default, it evaluates the first candlestick in the price_df.
    index = 0
    if date_or_index:
        # Index.
        if type(date_or_index) == int:
            index = date_or_index
            if index < 0 or index > len(price_df) - 1:
                return None
        # Date.
        if type(date_or_index) == str:
            index = price_df.index[price_df["date"] == date_or_index]
            if len(index) > 0:
                index = index[0]
            else:
                return None

    date = price_df.iloc[index]["date"]
    stock_code = price_df.iloc[index]["ticker"]

    if index + fut_size > len(price_df):
        print("{stock_code} does not have {fut_size} future candlesticks."
              .format(fut_size=fut_size, stock_code=stock_code))
        return None

    price = price_df.iloc[index]["close"]
    if a_share:
        fut_price_df = price_df.iloc[index + 1:index + fut_size - 1]
    else:
        fut_price_df = price_df.iloc[index:index + fut_size]

    max_fut_price = round(fut_price_df[key].max(), 3)
    result = {"stock_code": stock_code, "date": date, "fut_size": fut_size, "key": key, "a_share": a_share,
              "bullish_days": fut_price_df[key].ge(price).sum(),
              "bullish_trend": is_bullish_or_bearish_trend(fut_price_df.to_dict(orient="records"), key=key),
              "highest_price": max_fut_price,
              "highest_percent": round(max_fut_price / price - 1, 3),
              }

    return result


def evaluate_bullish_trend(price_df, params):
    pass


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
