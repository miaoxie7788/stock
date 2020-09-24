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


def is_bullish_or_bearish_trend(prices, key="close"):
    """
        A couple of consecutive daily prices (by default close prices) are fitted with a 1st order linear model y = ax
        + b. If a > 0, the trend is bullish otherwise bearish.

        price = {"open": y1, "close": y2, "high": y3, "low": y4}
    """
    close_prices = [price[key] for price in prices if not np.isnan(price[key])]

    n = len(close_prices)
    if n <= 1:
        return None

    x = np.array(range(1, n + 1))
    y = np.array(close_prices)

    slope, _ = list(np.polyfit(x, y, 1))
    if slope > 0:
        return "bullish"
    return "bearish"


def is_hammer(price, low_th=0.02, body_th=0.5, high_th=0.01):
    """
        A black or a white candlestick that consists of a small body near the high with a little or no upper shadow and
        a long lower tail. Considered a bullish pattern during a downtrend.

        price = {"open": y1, "close": y2, "high": y3, "low": y4}
    """
    y1, y2, y3, y4 = price['open'], price['close'], price['high'], price['low']

    d1 = y3 - y2
    d2 = y2 - y1
    d3 = y1 - y4

    if d2 > 0:
        if (d3 / y1 >= low_th) and (d2 / d3 <= body_th) and (d1 / y2 <= high_th):
            return True

    return False


def is_inverted_hammer(price, low_th=0.01, body_th=0.5, high_th=0.02):
    """
        A black or a white candlestick in an upside-down hammer position.

        price = {"open": y1, "close": y2, "high": y3, "low": y4}
    """
    y1, y2, y3, y4 = price['open'], price['close'], price['high'], price['low']

    d1 = y3 - y2
    d2 = y2 - y1
    d3 = y1 - y4

    if d2 > 0:
        if (d3 / y1 <= low_th) and (d2 / d1 <= body_th) and (d1 / y2 >= high_th):
            return True

    return False


def detect_hammer(price_df, window_size=5):
    """
        Detect hammers.
    """

    df["is_hammer"] = price_df.apply(is_hammer, axis="columns")
    neighbour_prices_dict = dict()
    for _, price in df[df.is_hammer].iterrows():
        x = price.name
        if x >= window_size:
            hist_prices = price_df.iloc[x - window_size:x + 1].to_dict(orient="records")
            if is_bullish_or_bearish_trend(hist_prices) == "bearish":
                print("A bullish trend reversal is signaled at {date}".format(date=price["date"]))
                neighbour_prices_dict[price["date"]] = price_df.iloc[x - window_size:x + window_size]

    plot_candlestick(neighbour_prices_dict["2018-04-27"])


def plot_candlestick(price_df):
    fig = go.Figure(data=[go.Candlestick(
        x=price_df['date'],
        open=price_df['open'],
        high=price_df['high'],
        low=price_df['low'],
        close=price_df['close'])])

    fig.show()


if __name__ == "__main__":
    # asx_stock_watchlist = ["tls.ax", "wbc.ax", "nov.ax", "cba.ax", "hack.ax", "ltr.ax"]

    # plot_candlestick("tls.ax")
    stock_code = "wbc.ax"
    stock_path = "data/asx_stock/csv"
    csv_filename = os.path.join(stock_path, stock_code, "hist_price_19880128_20200921.csv")
    df = pd.read_csv(csv_filename)
    detect_hammer(df, window_size=5)
