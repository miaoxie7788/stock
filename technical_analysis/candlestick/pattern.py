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
    prices = [candlestick[key] for candlestick in candlesticks if not np.isnan(candlestick[key])]

    n = len(prices)
    if n <= 1:
        return None

    x = np.array(range(1, n + 1))
    y = np.array(prices)

    slope, _ = list(np.polyfit(x, y, 1))
    if slope > 0:
        return "bullish"
    return "bearish"


def is_market_bottom(candlesticks, key="low"):
    """
        A couple of consecutive daily prices (by default low prices) present a bearish_trend.
        If the latest daily price is minimal, it is a market bottom; otherwise not.
    """
    present_candlestick = candlesticks[-1]
    history_candlesticks = candlesticks[:-1]

    if is_bullish_or_bearish_trend(history_candlesticks) == "bearish":
        present_price = present_candlestick[key]
        history_prices = [candlestick[key] for candlestick in history_candlesticks if not np.isnan(candlestick[key])]

        if present_price <= min(history_prices):
            return True

    return False


# Simple candlestick patterns.
def is_big_black_candle(candlestick, t1, t3, long_body=0.05):
    """
        Big Black Candle has an unusually long black body with a wide range between high and low. Prices open near the
        high and close near the low. Considered a bearish pattern.
    """
    if is_bullish_or_bearish_candlestick(candlestick) != "bearish":
        return False

    y1, y2, _, _, d1, d2, d3 = extract_candlestick(candlestick)

    if 2 * d2 / (y1 + y2) <= long_body:
        return False

    if d1 > 0 and d2 > 0 and d3 > 0:
        if d2 / d1 > t1 and d2 / d3 > t3:
            return True

    return False


def is_big_white_candle(candlestick, t1, t3, long_body=0.05):
    """
        Big White Candle Has an unusually long white body with a wide range between high and low of the day. Prices
        open near the low and close near the high. Considered a bullish pattern.
    """
    if is_bullish_or_bearish_candlestick(candlestick) != "bullish":
        return False

    y1, y2, _, _, d1, d2, d3 = extract_candlestick(candlestick)

    if 2 * d2 / (y1 + y2) <= long_body:
        return False

    if d1 > 0 and d2 > 0 and d3 > 0:
        if d2 / d1 > t1 and d2 / d3 > t3:
            return True

    return False


def is_black_body():
    """
        Black Body Formed when the opening price is higher than the closing price. Considered to be a bearish signal.
    """
    pass


def is_white_body():
    """
        White Body Formed when the closing price is higher than the opening price and considered a bullish signal.
    """
    pass


def is_doji(candlestick):
    """
        Doji Formed when opening and closing prices are virtually the same. The lengths of shadows can vary.
    """
    _, _, _, _, d1, d2, d3 = extract_candlestick(candlestick)

    if d1 > 0 and d2 == 0 and d3 > 0:
        return True

    return False


def is_long_legged_doji(candlestick, long_upper_shadow, long_lower_shadow):
    """
        Long-Legged Doji Consists of a Doji with very long upper and lower shadows. Indicates strong forces balanced in
        opposition.
    """
    pass


def is_dragonfly_doji(candlestick, long_lower_shadow=0.05):
    """
        Dragonfly Doji Formed when the opening and the closing prices are at the highest of the day. If it has a longer
        lower shadow it signals a more bullish trend. When appearing at market bottoms it is considered to be a reversal
        signal.
    """
    y1, y2, _, _, d1, d2, d3 = extract_candlestick(candlestick)

    if d1 == 0 and d2 == 0:
        if 2 * d3 / (y1 + y2) > long_lower_shadow:
            return True

    return False


def is_gravestone_doji(candlestick, long_upper_shadow=0.05):
    """
        Formed when the opening and closing prices are at the lowest of the day. If it has a longer upper shadow it
        signals a bearish trend. When it appears at market top it is considered a reversal signal.
    """
    y1, y2, _, _, d1, d2, d3 = extract_candlestick(candlestick)

    if d2 == 0 and d3 == 0:
        if 2 * d1 / (y1 + y2) > long_upper_shadow:
            return True

    return False


def is_hammer(candlestick, t1, t3, small_body=0.01):
    """
        A black or a white candlestick that consists of a small body near the high with a little or no upper shadow and
        a long lower tail. Considered a bullish pattern during a downtrend.
    """
    y1, y2, _, _, d1, d2, d3 = extract_candlestick(candlestick)

    if 2 * d2 / (y1 + y2) > small_body:
        return False

    if d1 > 0 and d2 > 0 and d3 > 0:
        if d2 / d1 > t1 and d3 / d2 > t3:
            return True

    return False


def is_inverted_hammer(candlestick, t1, t3, small_body=0.01):
    """
        A black or a white candlestick in an upside-down hammer position.
    """
    y1, y2, _, _, d1, d2, d3 = extract_candlestick(candlestick)

    if 2 * d2 / (y1 + y2) > small_body:
        return False

    if d1 > 0 and d2 > 0 and d3 > 0:
        if d1 / d2 > t1 and d2 / d3 > t3:
            return True

    return False


# Complex candlestick patterns.

# Reversal signals.
def is_dragonfly_doji_reversal(candlesticks, long_lower_shadow):
    """
        When appearing at market bottoms it is considered to be a reversal signal (bullish).
    """

    present_candlestick = candlesticks[-1]

    if is_market_bottom(candlesticks) and is_dragonfly_doji(present_candlestick, long_lower_shadow=long_lower_shadow):
        return True

    return False
