"""
    Candlestick techniques, signals

    reference:
    https://www.ig.com/au/trading-strategies/16-candlestick-patterns-every-trader-should-know-180615
    https://www.investopedia.com/articles/active-trading/092315/5-most-powerful-candlestick-patterns.asp
"""

from candlestick.core.pattern import is_hammer, is_inverted_hammer
from candlestick.core.trend import is_market_top_or_bottom


# bullish
def is_hammer_signal(cur_candlestick, his_candlesticks, abs_slope, t1, t3, small_body):
    """
         The hammer candlestick pattern is formed of a short body with a long lower wick, and is found at the bottom
         of a downward trend.

         A hammer shows that although there were selling pressures during the day, ultimately a strong buying
         pressure drove the price back up. The colour of the body can vary, but green hammers indicate a stronger
         bull market than red hammers.
    """

    if is_market_top_or_bottom(cur_candlestick, his_candlesticks, "low", abs_slope) == "bottom" and \
            is_hammer(cur_candlestick, t1, t3, small_body):
        return True

    return False


def is_inverted_hammer_signal(cur_candlestick, his_candlesticks, abs_slope, t1, t3, small_body):
    """
        A similarly bullish pattern is the inverted hammer. The only difference being that the upper wick is long,
        while the lower wick is short.

        It indicates a buying pressure, followed by a selling pressure that was not strong enough to drive the market
        price down. The inverse hammer suggests that buyers will soon have control of the market.
    """

    if is_market_top_or_bottom(cur_candlestick, his_candlesticks, "low", abs_slope) == "bottom" and \
            is_inverted_hammer(cur_candlestick, t1, t3, small_body):
        return True

    return False


def is_bullish_engulfing_signal():
    pass
