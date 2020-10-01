from technical_analysis.candlestick.pattern import is_hammer, is_dragonfly_doji, is_gravestone_doji
from technical_analysis.candlestick.trend import is_market_bottom, is_market_top, is_bullish_or_bearish_trend


# Bullish or bearish patterns.
# TODO it should create another function to determine downtrend/uptrend, which might be different from
#  bullish/bearish trend.
def is_hammer_bullish_pattern(candlesticks, t1, t3, small_body):
    """
         Considered a bullish pattern during a downtrend.
    """

    present_candlestick = candlesticks[-1]

    if is_bullish_or_bearish_trend(candlesticks) == "bearish" and is_hammer(present_candlestick, t1, t3, small_body):
        return True

    return False


# Reversal signals.
def is_dragonfly_doji_reversal(candlesticks, long_lower_shadow):
    """
        When appearing at market bottoms it is considered to be a reversal signal (bullish).
    """

    present_candlestick = candlesticks[-1]

    if is_market_bottom(candlesticks) and is_dragonfly_doji(present_candlestick, long_lower_shadow):
        return True

    return False


def is_gravestone_doji_reversal(candlesticks, long_upper_shadow):
    """
        When it appears at market top it is considered a reversal signal (bearish).
    """
    present_candlestick = candlesticks[-1]

    if is_market_top(candlesticks) and is_gravestone_doji(present_candlestick, long_upper_shadow=long_upper_shadow):
        return True

    return False
