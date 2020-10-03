"""
    Candlestick techniques, signals

    reference:
    https://www.ig.com/au/trading-strategies/16-candlestick-patterns-every-trader-should-know-180615
    https://www.investopedia.com/articles/active-trading/092315/5-most-powerful-candlestick-patterns.asp
"""

from technical_analysis.candlestick.pattern import is_hammer, is_dragonfly_doji, is_gravestone_doji
from technical_analysis.candlestick.trend import is_market_bottom, is_market_top


# bullish
def is_hammer_reversal(candlesticks, t1, t3, small_body):
    """
         The hammer candlestick pattern is formed of a short body with a long lower wick, and is found at the bottom
         of a downward trend.

         A hammer shows that although there were selling pressures during the day, ultimately a strong buying
         pressure drove the price back up. The colour of the body can vary, but green hammers indicate a stronger
         bull market than red hammers.
    """

    present_candlestick = candlesticks[-1]

    if is_market_bottom(candlesticks) and is_hammer(present_candlestick, t1, t3, small_body):
        return True

    return False


def is_inverted_hammer_reversal():
    """
        A similarly bullish pattern is the inverted hammer. The only difference being that the upper wick is long,
        while the lower wick is short.

        It indicates a buying pressure, followed by a selling pressure that was not strong enough to drive the market
        price down. The inverse hammer suggests that buyers will soon have control of the market.
    """
    pass


def is_bullish_engulfing_signal():
    pass


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