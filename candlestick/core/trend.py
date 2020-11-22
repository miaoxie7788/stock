"""
    Candlestick techniques, trends

"""

import numpy as np


def is_bullish_or_bearish_trend(candlesticks, key="close"):
    """
        A couple of consecutive daily/weekly/monthly prices (by default close prices) are fitted with a 1st order
        linear model y = ax + b. If a > 0, the trend is bullish otherwise bearish.

        :param candlesticks:        A list of candlesticks.
        :param key:                 "high" | "low" | "open" | "close"
        :return:                    "bullish" | "bearish", degree
    """
    prices = [candlestick[key] for candlestick in candlesticks if not np.isnan(candlestick[key])]

    n = len(prices)
    if n <= 1:
        return None, None

    x = np.array(range(1, n + 1))
    y = np.array(prices)

    slope, _ = list(np.polyfit(x, y, 1))
    degree = np.degrees(np.arctan(slope))

    if degree > 0:
        bullish_or_bearish = "bullish"
    else:
        bullish_or_bearish = "bearish"

    return bullish_or_bearish, degree


def is_market_top_or_bottom(candlestick, ref_candlesticks, key="low"):
    """
        A couple of consecutive daily prices (by default low prices) present a bullish/bearish_trend.
        If the latest daily price is maximal/minimal, it is a market top/bottom; otherwise None.
    """

    price = candlestick[key]
    ref_prices = [candlestick[key] for candlestick in ref_candlesticks if not np.isnan(candlestick[key])]

    bullish_or_bearish, _ = is_bullish_or_bearish_trend(candlesticks=ref_candlesticks, key="close")

    top_or_bottom = None
    if bullish_or_bearish == "bullish" and price >= max(ref_prices):
        top_or_bottom = "top"

    if bullish_or_bearish == "bearish" and price <= min(ref_prices):
        top_or_bottom = "bottom"

    return top_or_bottom
