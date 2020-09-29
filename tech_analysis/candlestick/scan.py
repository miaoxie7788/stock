"""
    Scan candlestick patterns.
"""
import os

import pandas as pd
import plotly.graph_objects as go

from tech_analysis.candlestick.pattern import is_hammer, is_bullish_or_bearish_trend


# TODO: move the scan functions to integration test.


def scan_hammer(price_df, window_size=5):
    """
        Scan hammers.
    """

    def parameterised_is_hammer(candlestick):
        return is_hammer(candlestick, t1=4, t3=2, small_body=0.01)

    df["is_hammer"] = price_df.apply(parameterised_is_hammer, axis="columns")
    neighbour_prices_dict = dict()
    for _, price in df[df.is_hammer].iterrows():
        x = price.name
        if x >= window_size:
            hist_prices = price_df.iloc[x - window_size:x + 1].to_dict(orient="records")
            if is_bullish_or_bearish_trend(hist_prices) == "bearish":
                # print("A bullish trend reversal is signaled on {date}".format(date=price["date"]))
                neighbour_prices_dict[price["date"]] = price_df.iloc[x - window_size:x + window_size]

    n = len(neighbour_prices_dict)
    print("There are a total of {n} reversals.".format(n=n))

    # Verify the effectiveness:
    effective = 0
    for date, neighbour_prices in neighbour_prices_dict.items():
        future_prices = neighbour_prices.iloc[window_size:].to_dict(orient="records")

        if is_bullish_or_bearish_trend(future_prices) == "bullish":
            effective += 1
            print("It is effective on {date}".format(date=date))
        else:
            print("It is not effective on {date}".format(date=date))

    print("The successful rate is: {rate}".format(rate=effective / n))
    # plot_candlestick(neighbour_prices_dict["1999-05-12"])


# def scan_inverted_hammer(price_df, window_size=5):
#     """
#         Scan inverted hammers.
#     """
#
#     def parameterised_is_inverted_hammer(candlestick):
#         return is_inverted_hammer(candlestick, t1=0.01, t2=0.002, t3=0.001)
#
#     df["is_inverted_hammer"] = price_df.apply(parameterised_is_inverted_hammer, axis="columns")
#     neighbour_prices_dict = dict()
#     for _, price in df[df.is_inverted_hammer].iterrows():
#         x = price.name
#         if x >= window_size:
#             hist_prices = price_df.iloc[x - window_size:x + 1].to_dict(orient="records")
#             if is_bullish_or_bearish_trend(hist_prices) == "bullish":
#                 print("A bearish trend reversal is signaled at {date}".format(date=price["date"]))
#                 neighbour_prices_dict[price["date"]] = price_df.iloc[x - window_size:x + window_size]
#
#     n = len(neighbour_prices_dict)
#     print("There are a total of {n} reversals.".format(n=n))
#
#     # Verify the effectiveness:
#     effective = 0
#     for date, neighbour_prices in neighbour_prices_dict.items():
#         future_prices = neighbour_prices.iloc[window_size:].to_dict(orient="records")
#
#         if is_bullish_or_bearish_trend(future_prices) == "bearish":
#             effective += 1
#             print("It is effective on {date}".format(date=date))
#         else:
#             print("It is not effective on {date}".format(date=date))
#
#     print("The successful rate is: {rate}".format(rate=effective / n))
#
#     # plot_candlestick(neighbour_prices_dict["2008-04-24"])


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
    stock_path = "data/asx_stock/csv"

    wbc = "wbc.ax"
    # df = pd.read_csv(os.path.join(stock_path, wbc, "hist_price_19880128_20200921.csv"))
    # scan_hammer(df, window_size=5)
    # scan_inverted_hammer(df, window_size=5)
    # scan_dragonfly_doji(df, window_size=3)

    tls = "tls.ax"
    df = pd.read_csv(os.path.join(stock_path, tls, "hist_price_19971127_20200921.csv"))
    # scan_hammer(df, window_size=7)
    # scan_inverted_hammer(df, window_size=5)
    scan_dragonfly_doji(df, window_size=7)
