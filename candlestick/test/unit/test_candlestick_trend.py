import unittest

from candlestick.core.trend import is_bullish_or_bearish_trend


class TestCandlestickPattern(unittest.TestCase):

    def test_is_bullish_or_bearish_trend(self):
        candlesticks = [
            {'open': 5.0, 'close': 5.5, 'high': 5.4, 'low': 4.8},
            {'open': 5.1, 'close': 5.55, 'high': 5.65, 'low': 4.85},
            {'open': 5.05, 'close': 5.5, 'high': 5.55, 'low': 4.65},
            {'open': 4.7, 'close': 5.65, 'high': 5.85, 'low': 4.75},
            {'open': 5.3, 'close': 5.7, 'high': 5.95, 'low': 4.95},
        ]

        print(is_bullish_or_bearish_trend(candlesticks=candlesticks, key="high"))
        self.assertEqual(is_bullish_or_bearish_trend(candlesticks=candlesticks, key="close")[0], "bullish")


if __name__ == '__main__':
    unittest.main()
