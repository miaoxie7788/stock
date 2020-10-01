# Reversal signals.
def is_dragonfly_doji_reversal(candlesticks, long_lower_shadow):
    """
        When appearing at market bottoms it is considered to be a reversal signal (bullish).
    """

    present_candlestick = candlesticks[-1]

    if is_market_bottom(candlesticks) and is_dragonfly_doji(present_candlestick, long_lower_shadow=long_lower_shadow):
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
