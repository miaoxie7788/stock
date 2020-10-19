"""
    Candlestick techniques, trends

"""

import numpy as np


def is_bullish_or_bearish_trend(candlesticks, key="close", abs_slope=0):
    """
        A couple of consecutive daily prices (by default close prices) are fitted with a 1st order linear model y = ax
        + b. If a > 0, the trend is bullish otherwise bearish.
    """
    prices = [candlestick[key] for candlestick in candlesticks if not np.isnan(candlestick[key])]

    n = len(prices)
    if n <= 1:
        return None

    x = np.array(range(1, n + 1))
    y = np.array(prices)

    slope, _ = list(np.polyfit(x, y, 1))
    if slope > abs_slope:
        return "bullish"

    if slope < 0 and abs(slope) > abs_slope:
        return "bearish"

    return None


def is_market_top_or_bottom(candlestick, ref_candlesticks, key="low", abs_slope=0):
    """
        A couple of consecutive daily prices (by default low prices) present a bullish/bearish_trend.
        If the latest daily price is maximal/minimal, it is a market top/bottom; otherwise None.
    """

    price = candlestick[key]
    ref_prices = [candlestick[key] for candlestick in ref_candlesticks if not np.isnan(candlestick[key])]

    if is_bullish_or_bearish_trend(ref_candlesticks, "close", abs_slope) == "bullish" \
            and price >= max(ref_prices):
        return "top"

    if is_bullish_or_bearish_trend(ref_candlesticks, "close", abs_slope) == "bearish" \
            and price <= min(ref_prices):
        return "bottom"

    return None
