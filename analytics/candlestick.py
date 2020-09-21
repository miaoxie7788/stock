"""
    Candlestick techniques

    reference:
    https://en.wikipedia.org/wiki/Candlestick_pattern
    https://www.ig.com/au/trading-strategies/16-candlestick-patterns-every-trader-should-know-180615
    https://www.investopedia.com/articles/active-trading/092315/5-most-powerful-candlestick-patterns.asp
"""

import os

import pandas as pd
import plotly.graph_objects as go


def is_pattern_hammer(price, low_th=0.02, body_th=0.5, high_th=0.1):
    """
        A black or a white candlestick that consists of a small body near the high with a little or no upper shadow and
        a long lower tail. Considered a bullish pattern during a downtrend.

        (close - low) / low >= low_deviation
        (open - close) / low_deviation <= body
        (high - open) / low_deviation <= high_deviation
    """
    open_price, close_price, high_price, low_price = price['open'], price['close'], price['high'], price['low']

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
    for _, price in df.iterrows():
        # print(price)
        a = is_pattern_hammer(price)
        if a:
            k += 1
            print(price)
    print(k)

    plot_candlestick(stock_code, stock_path="data/asx_stock/csv")
