"""
    Candlestick techniques

    reference:
    https://en.wikipedia.org/wiki/Candlestick_pattern
    https://www.ig.com/au/trading-strategies/16-candlestick-patterns-every-trader-should-know-180615
    https://www.investopedia.com/articles/active-trading/092315/5-most-powerful-candlestick-patterns.asp
"""

import os

import numpy as np
import pandas as pd
import plotly.graph_objects as go


def is_trend_bullish(daily_prices):
    """
        A couple of consecutive daily close prices are fitted with a 1st order linear model y = ax + b.
        If a > 0, the trend is bullish otherwise bearish.
    """
    close_prices = [daily_price["close"] for daily_price in daily_prices if not np.isnan(daily_price["close"])]

    n = len(close_prices)
    if n <= 1:
        return None

    x = np.array(range(1, n + 1))
    y = np.array(close_prices)

    slope, _ = list(np.polyfit(x, y, 1))
    if slope > 0:
        return True
    return False


def is_pattern_hammer(daily_price, low_th=0.02, body_th=0.5, high_th=0.1):
    """
        A black or a white candlestick that consists of a small body near the high with a little or no upper shadow and
        a long lower tail. Considered a bullish pattern during a downtrend.

        (close - low) / low >= low_deviation
        (open - close) / low_deviation <= body
        (high - open) / low_deviation <= high_deviation
    """
    open_price = daily_price['open']
    close_price = daily_price['close']
    high_price = daily_price['high']
    low_price = daily_price['low']

    x = high_price - open_price
    y = open_price - close_price
    z = close_price - low_price

    if y > 0:
        if (z / low_price >= low_th) and (y / z <= body_th) and (x / z <= high_th):
            return True

    return False


# def detect_pattern_hammer(price_df):


def plot_candlestick(stock_code, stock_path="data/asx_stock/csv"):
    csv_filename = os.path.join(stock_path, stock_code, "hist_price_19971127_20200921.csv")
    df = pd.read_csv(csv_filename)
    # df = df.iloc[-30:]
    # print(df)
    fig = go.Figure(data=[go.Candlestick(
        x=df['date'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'])])

    fig.show()


if __name__ == "__main__":
    # asx_stock_watchlist = ["tls.ax", "wbc.ax", "nov.ax", "cba.ax", "hack.ax", "ltr.ax"]

    # plot_candlestick("tls.ax")
    stock_code = "tls.ax"
    stock_path = "data/asx_stock/csv"
    csv_filename = os.path.join(stock_path, stock_code, "hist_price_19971127_20200921.csv")
    df = pd.read_csv(csv_filename)

    k = 0
    for t, price in df.iterrows():

        hammer = is_pattern_hammer(price)
        if hammer:
            hist_prices = list(df.iloc[t - 3: t].T.to_dict().values())
            if not is_trend_bullish(hist_prices):
                k += 1
                print("a turning point is found.")
                print(price)
                close_prices = [hist_price["close"] for hist_price in hist_prices if not np.isnan(hist_price["close"])]
                print(close_prices)
                print("\n")
    print(k)

    plot_candlestick(stock_code, stock_path="data/asx_stock/csv")
