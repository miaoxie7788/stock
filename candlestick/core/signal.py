"""
    Candlestick techniques, signals

    reference:
    https://www.ig.com/au/trading-strategies/16-candlestick-patterns-every-trader-should-know-180615
    https://www.investopedia.com/articles/active-trading/092315/5-most-powerful-candlestick-patterns.asp
"""

from candlestick.core.pattern import is_bullish_or_bearish_candlestick, is_hammer, is_inverted_hammer
from candlestick.core.trend import is_market_top_or_bottom


# bullish
def is_hammer_signal(cur_candlestick, his_candlesticks, abs_slope, t1, t3, small_body, enhanced=False):
    """
         The hammer candlestick pattern is formed of a short body with a long lower wick, and is found at the bottom
         of a downward trend.

         A hammer shows that although there were selling pressures during the day, ultimately a strong buying
         pressure drove the price back up. The colour of the body can vary, but green hammers indicate a stronger
         bull market than red hammers.
    """

    c1 = is_market_top_or_bottom(cur_candlestick, his_candlesticks, "low", abs_slope) == "bottom"
    c2 = is_hammer(cur_candlestick, t1, t3, small_body)

    if not enhanced:
        if c1 and c2:
            return True
    else:
        c3 = is_bullish_or_bearish_candlestick(cur_candlestick) == "bullish"
        if c1 and c2 and c3:
            return True

    return False


def is_inverted_hammer_signal(cur_candlestick, his_candlesticks, abs_slope, t1, t3, small_body, enhanced=False):
    """
        A similarly bullish pattern is the inverted hammer. The only difference being that the upper wick is long,
        while the lower wick is short.

        It indicates a buying pressure, followed by a selling pressure that was not strong enough to drive the market
        price down. The inverse hammer suggests that buyers will soon have control of the market.
    """

    c1 = is_market_top_or_bottom(cur_candlestick, his_candlesticks, "low", abs_slope) == "bottom"
    c2 = is_inverted_hammer(cur_candlestick, t1, t3, small_body)

    if not enhanced:
        if c1 and c2:
            return True
    else:
        c3 = is_bullish_or_bearish_candlestick(cur_candlestick) == "bullish"
        if c1 and c2 and c3:
            return True

    return False


def is_bullish_engulfing_signal():
    pass
