"""
    Candlestick techniques

    reference:
    https://en.wikipedia.org/wiki/Candlestick_pattern
    https://www.ig.com/au/trading-strategies/16-candlestick-patterns-every-trader-should-know-180615
    https://www.investopedia.com/articles/active-trading/092315/5-most-powerful-candlestick-patterns.asp
"""

from technical_analysis.candlestick.trend import is_bullish_or_bearish_candlestick, extract_candlestick


# Simple candlestick patterns.
def is_big_black_candle(candlestick, t1=5, t3=5, long_body=0.05):
    """
        Has an unusually long black body with a wide range between high and low. Prices open near the high and close
        near the low. Considered a bearish pattern.
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


def is_big_white_candle(candlestick, t1=5, t3=5, long_body=0.05):
    """
        Has an unusually long white body with a wide range between high and low of the day. Prices open near the low
        and close near the high. Considered a bullish pattern.
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
        Formed when the opening price is higher than the closing price. Considered to be a bearish signal.
    """
    pass


def is_white_body():
    """
        Formed when the closing price is higher than the opening price and considered a bullish signal.
    """
    pass


def is_doji(candlestick):
    """
        Formed when opening and closing prices are virtually the same. The lengths of shadows can vary.
    """
    _, _, _, _, d1, d2, d3 = extract_candlestick(candlestick)

    if d1 > 0 and d2 == 0 and d3 > 0:
        return True

    return False


def is_long_legged_doji(candlestick, long_upper_shadow, long_lower_shadow):
    """
        Consists of a Doji with very long upper and lower shadows. Indicates strong forces balanced in
        opposition.
    """
    pass


def is_dragonfly_doji(candlestick, long_lower_shadow=0.05):
    """
        Formed when the opening and the closing prices are at the highest of the day. If it has a longer lower shadow
        it signals a more bullish trend. When appearing at market bottoms it is considered to be a reversal signal.
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


def is_hammer(candlestick, t1=10, t3=3, small_body=0.01):
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


def is_inverted_hammer(candlestick, t1=3, t3=10, small_body=0.01):
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


def is_hanging_man(candlestick, t1=10, small_body=0.01):
    """
        A black or a white candlestick that consists of a small body near the high with a little or no
        upper shadow and a long lower tail. The lower tail should be two or three times the height of the body.
        Considered a bearish pattern during an uptrend.
    """

    y1, y2, _, _, d1, d2, d3 = extract_candlestick(candlestick)

    if 2 * d2 / (y1 + y2) > small_body:
        return False

    if d1 >= 0 and d2 > 0 and d3 > 0:
        if d2 / d1 > t1 and 2 <= d3 / d2 <= 3:
            return True

    return False

# Complex candlestick patterns.
