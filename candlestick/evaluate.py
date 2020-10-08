import numpy as np
import pandas as pd
import plotly.graph_objects as go


def plot_candlestick(candlestick_df):
    fig = go.Figure(data=[go.Candlestick(
        x=candlestick_df['date'],
        open=candlestick_df['open'],
        high=candlestick_df['high'],
        low=candlestick_df['low'],
        close=candlestick_df['close'])])

    fig.show()


def debug(window_df):
    while True:
        date = input("Type the date to plot its neighbouring candlesticks: \n")
        window = window_df.loc[window_df["date"] == date]

        candlesticks = [*window['his'].values[0], window['cur'].values[0], *window['fut'].values[0]]
        plot_candlestick(pd.DataFrame(candlesticks))


def evaluate_any_higher_price(windows, key="close"):
    """"
        Each window is a dict of date, his_candlesticks, cur_candlestick, fut_candlesticks.

        E.g., his_size = 3, fut_size = 2, cur_candlestick = c0
        c-3, c-2, c-1, c0, c1, c2

        It evaluates if there is any price of [c1, c2] (by default close price) higher than price of c0. If yes,
        it indicates "success"; otherwise "failure".
    """

    def any_higher_price(row):
        fut_prices = [candlestick[key] for candlestick in row["fut"] if not np.isnan(candlestick[key])]
        if fut_prices:
            max_fut_price = max(fut_prices)
        else:
            max_fut_price = 0
        cut_price = row["cur"][key]

        return round(max_fut_price / cut_price - 1, 3)

    windows_df = pd.DataFrame(windows)
    windows_df["higher_fut_price"] = windows_df.apply(any_higher_price, axis="columns")

    return windows_df


def evaluate_bullish_trend(windows, key="close", print_detail=True):
    pass
