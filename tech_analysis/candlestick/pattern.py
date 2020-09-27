"""
    Candlestick techniques

    reference:
    https://en.wikipedia.org/wiki/Candlestick_pattern
    https://www.ig.com/au/trading-strategies/16-candlestick-patterns-every-trader-should-know-180615
    https://www.investopedia.com/articles/active-trading/092315/5-most-powerful-candlestick-patterns.asp
"""

import numpy as np


def extract_candlestick(candlestick):
    """
        Extract prices and price differences from a bullish or bearish candlestick.

        candlestick = {"open": y1, "close": y2, "high": y3, "low": y4}
    """
    y1, y2, y3, y4 = candlestick['open'], candlestick['close'], candlestick['high'], candlestick['low']

    if is_bullish_or_bearish_candlestick(candlestick) == "bullish":
        d1, d2, d3 = y3 - y2, y2 - y1, y1 - y4
    else:
        d1, d2, d3 = y3 - y1, y1 - y2, y2 - y4

    return y1, y2, y3, y4, d1, d2, d3


def is_bullish_or_bearish_candlestick(candlestick):
    if candlestick["close"] >= candlestick["open"]:
        return "bullish"
    return "bearish"


def is_bullish_or_bearish_trend(candlesticks, key="close"):
    """
        A couple of consecutive daily prices (by default close prices) are fitted with a 1st order linear model y = ax
        + b. If a > 0, the trend is bullish otherwise bearish.
    """
    close_prices = [price[key] for price in candlesticks if not np.isnan(price[key])]

    n = len(close_prices)
    if n <= 1:
        return None

    x = np.array(range(1, n + 1))
    y = np.array(close_prices)

    slope, _ = list(np.polyfit(x, y, 1))
    if slope > 0:
        return "bullish"
    return "bearish"


# Simple patterns.
def is_big_black_candle(candlestick, t1, t2, t3):
    """
        Big Black Candle has an unusually long black body with a wide range between high and low. Prices open near the
        high and close near the low. Considered a bearish pattern.
    """
    if is_bullish_or_bearish_candlestick(candlestick) != "bearish":
        return False

    y1, y2, y3, y4, d1, d2, d3 = extract_candlestick(candlestick)

    if d1 > 0 and d2 > 0 and d3 > 0:
        if (d1 / y1 <= t1) and (d2 / y1 > t2) and (d3 / y2 <= t3):
            return True

    return False


def is_big_white_candle(candlestick, t1, t2, t3):
    """
        Big White Candle Has an unusually long white body with a wide range between high and low of the day. Prices
        open near the low and close near the high. Considered a bullish pattern.
    """
    if is_bullish_or_bearish_candlestick(candlestick) != "bullish":
        return False

    y1, y2, y3, y4, d1, d2, d3 = extract_candlestick(candlestick)

    if d1 > 0 and d2 > 0 and d3 > 0:
        if (d1 / y2 <= t1) and (d2 / y1 > t2) and (d3 / y1 <= t3):
            return True

    return False


def is_hammer(candlestick, t1, t3):
    """
        A black or a white candlestick that consists of a small body near the high with a little or no upper shadow and
        a long lower tail. Considered a bullish pattern during a downtrend.
    """
    y1, y2, y3, y4, d1, d2, d3 = extract_candlestick(candlestick)

    if d1 > 0 and d2 > 0 and d3 > 0:
        if d2 / d1 > t1 and d3 / d2 > t3:
            return True

    return False


def is_inverted_hammer(candlestick, t1, t2, t3):
    """
        A black or a white candlestick in an upside-down hammer position.
    """
    y1, y2, y3, y4, d1, d2, d3 = extract_candlestick(candlestick)

    if d1 > 0 and d2 > 0:
        if is_bullish_or_bearish_candlestick(candlestick) == "bullish":
            if (d1 / y2 > t1) and (d2 / y1 <= t2) and (d3 / y1 <= t3):
                return True
        else:
            if (d1 / y1 > t1) and (d2 / y2 <= t2) and (d3 / y2 <= t3):
                return True

    return False

# Complex patterns.
