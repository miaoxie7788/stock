"""
    Candlestick techniques, patterns

    reference:
    https://en.wikipedia.org/wiki/Candlestick_pattern
"""


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


def is_black_body(candlestick):
    """
        Formed when the opening price is higher than the closing price. Considered to be a bearish signal.
    """
    pass


def is_white_body(candlestick):
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


def is_long_legged_doji(candlestick):
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


def is_hammer(candlestick, t1=10, t3=3, small_body=0.05):
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


def is_inverted_hammer(candlestick, t1=3, t3=10, small_body=0.05):
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


def is_shooting_star(candlestick):
    """
        A black or a white candlestick that has a small body, a long upper shadow and a little or no lower tail.
        Considered a bearish pattern in an uptrend.
    """
    pass


def is_long_upper_shadow(candlestick):
    """
        A black or a white candlestick with an upper shadow that has a length of 2/3 or more of the total range of
        the candlestick. Normally considered a bearish signal when it appears around price resistance levels.
    """
    pass


def is_long_lower_shadow(candlestick):
    """
        A black or a white candlestick is formed with a lower tail that has a length of 2/3 or more of the total
        range of the candlestick. Normally considered a bullish signal when it appears around price support levels
    """
    pass


def is_marubozu(candlestick):
    """
        A long or a normal candlestick (black or white) with no shadow or tail. The high and the lows represent the
        opening and the closing prices. Considered a continuation pattern.
    """
    pass


def is_spinning_top(candlestick):
    """
        A black or a white candlestick with a small body. The size of shadows can vary. Interpreted as a neutral
        pattern but gains importance when it is part of other formations.
    """
    pass


def is_shaven_head(candlestick):
    """
        A black or a white candlestick with no upper shadow. [Compared with hammer.]
    """
    pass


def is_shaven_bottom(candlestick):
    """
        A black or a white candlestick with no lower tail. [Compare with Inverted Hammer.]
    """
    pass

# Complex candlestick patterns.
