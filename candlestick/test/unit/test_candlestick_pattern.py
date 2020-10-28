import unittest

from candlestick.core.pattern import is_big_black_candle, is_big_white_candle, is_doji, is_dragonfly_doji, \
    is_gravestone_doji, is_hammer, \
    is_inverted_hammer, is_hanging_man


class TestCandlestickPattern(unittest.TestCase):

    def test_is_big_black_candle(self):
        candlestick = {'open': 5.0, 'close': 4.2, 'high': 5.02, 'low': 4.18}

        self.assertEqual(is_big_black_candle(candlestick, t1=5, t3=5, long_body=0.05), True)

    def test_is_big_white_candle(self):
        candlestick = {'open': 4.2, 'close': 5, 'high': 5.02, 'low': 4.18}

        self.assertEqual(is_big_white_candle(candlestick, t1=5, t3=5, long_body=0.05), True)

    def test_is_doji(self):
        candlestick = {'open': 5, 'close': 5, 'high': 5.02, 'low': 4.85}

        self.assertEqual(is_doji(candlestick), True)

    def test_is_dragonfly_doji(self):
        candlestick = {'open': 5, 'close': 5, 'high': 5, 'low': 4.2}

        self.assertEqual(is_dragonfly_doji(candlestick, long_lower_shadow=0.1), True)

    def test_is_gravestone_doji(self):
        candlestick = {'open': 5, 'close': 5, 'high': 5.8, 'low': 5}

        self.assertEqual(is_gravestone_doji(candlestick, long_upper_shadow=0.1), True)

    def test_is_bullish_hammer(self):
        candlestick = {'open': 5.1, 'close': 5.3, 'high': 5.32, 'low': 4.3}

        self.assertEqual(is_hammer(candlestick, t1=4, t3=2, small_body=0.05), True)

    def test_is_bearish_hammer(self):
        candlestick = {'open': 5.3, 'close': 5.1, 'high': 5.35, 'low': 4.3}

        self.assertEqual(is_hammer(candlestick, t1=4, t3=2, small_body=0.05), True)

    def test_is_bullish_inverted_hammer(self):
        candlestick = {'open': 5.1, 'close': 5.3, 'high': 5.9, 'low': 5.05}

        self.assertEqual(is_inverted_hammer(candlestick, t1=2, t3=4, small_body=0.05), True)

    def test_is_bearish_inverted_hammer(self):
        candlestick = {'open': 5.3, 'close': 5.1, 'high': 5.9, 'low': 5.05}

        self.assertEqual(is_inverted_hammer(candlestick, t1=2, t3=4, small_body=0.05), True)

    def test_is_bullish_hanging_man(self):
        candlestick = {'open': 5.15, 'close': 5.4, 'high': 5.41, 'low': 4.55}

        self.assertEqual(is_hanging_man(candlestick, t1=10, small_body=0.05), True)


if __name__ == '__main__':
    unittest.main()
