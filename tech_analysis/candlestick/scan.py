import os

import pandas as pd
import plotly.graph_objects as go

from tech_analysis.candlestick.pattern import is_hammer, is_inverted_hammer, is_bullish_or_bearish_trend


def scan_hammer(price_df, window_size=5):
    """
        Scan hammers.
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

    plot_candlestick(neighbour_prices_dict["2001-09-19"])


def scan_inverted_hammer(price_df, window_size=5):
    """
        Scan inverted hammers.
    """
    df["is_inverted_hammer"] = price_df.apply(is_inverted_hammer, axis="columns")
    neighbour_prices_dict = dict()
    for _, price in df[df.is_inverted_hammer].iterrows():
        x = price.name
        if x >= window_size:
            hist_prices = price_df.iloc[x - window_size:x + 1].to_dict(orient="records")
            if is_bullish_or_bearish_trend(hist_prices) == "bullish":
                print("A bearish trend reversal is signaled at {date}".format(date=price["date"]))
                neighbour_prices_dict[price["date"]] = price_df.iloc[x - window_size:x + window_size]

    # plot_candlestick(neighbour_prices_dict["2008-04-24"])


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
    scan_hammer(df, window_size=5)
    # scan_inverted_hammer(df, window_size=5)
