import unittest

from ta_candlestick.core.trend import is_bullish_or_bearish_trend, is_market_top_or_bottom


class TestCandlestickPattern(unittest.TestCase):

    def test_is_bullish_or_bearish_trend(self):
        candlesticks = [
            {'open': 5.0, 'close': 5.5, 'high': 5.4, 'low': 4.8},
            {'open': 5.1, 'close': 5.55, 'high': 5.65, 'low': 4.85},
            {'open': 5.05, 'close': 5.5, 'high': 5.55, 'low': 4.65},
            {'open': 4.7, 'close': 5.65, 'high': 5.85, 'low': 4.75},
            {'open': 5.3, 'close': 5.7, 'high': 5.95, 'low': 4.95},
        ]

        bullish_or_bearish, degree = is_bullish_or_bearish_trend(candlesticks=candlesticks, key="close")

        self.assertEqual(bullish_or_bearish, "bullish")

    def test_is_market_top_or_bottom(self):
        candlestick = {'open': 5.05, 'close': 4.55, 'high': 5.1, 'low': 4.5}

        ref_candlesticks = [
            {'open': 5.0, 'close': 5.5, 'high': 5.7, 'low': 4.8},
            {'open': 5.1, 'close': 5.45, 'high': 5.65, 'low': 4.7},
            {'open': 5.05, 'close': 5.5, 'high': 5.5, 'low': 4.55},
            {'open': 4.7, 'close': 5.4, 'high': 5.55, 'low': 4.65},
            {'open': 5.05, 'close': 5.1, 'high': 5.2, 'low': 4.6},
        ]

        top_or_bottom = is_market_top_or_bottom(candlestick=candlestick, ref_candlesticks=ref_candlesticks, key="low")

        self.assertEqual(top_or_bottom, "bottom")


if __name__ == '__main__':
    unittest.main()
