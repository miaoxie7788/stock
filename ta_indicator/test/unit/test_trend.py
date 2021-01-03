import unittest

from ta_indicator.trend import is_upward_or_downward_trend, is_market_top_or_bottom


class TestCandlestickPattern(unittest.TestCase):

    def test_is_upward_or_downward_trend(self):
        y = [5.5, 5.55, 5.5, 5.65, 5.7]
        upward_or_downward, degree = is_upward_or_downward_trend(y)

        self.assertEqual(upward_or_downward, "upward")

    def test_is_market_top_or_bottom(self):
        candlesticks = [
            {'open': 5.0, 'close': 5.5, 'high': 5.7, 'low': 4.8},
            {'open': 5.1, 'close': 5.45, 'high': 5.65, 'low': 4.7},
            {'open': 5.05, 'close': 5.5, 'high': 5.5, 'low': 4.55},
            {'open': 4.7, 'close': 5.4, 'high': 5.55, 'low': 4.65},
            {'open': 5.05, 'close': 5.1, 'high': 5.2, 'low': 4.6},
        ]

        y = [candlestick['close'] for candlestick in candlesticks]
        trend_y = [candlestick['low'] for candlestick in candlesticks]

        top_or_bottom = is_market_top_or_bottom(trend_y, y)

        self.assertEqual(top_or_bottom, "bottom")


if __name__ == '__main__':
    unittest.main()
