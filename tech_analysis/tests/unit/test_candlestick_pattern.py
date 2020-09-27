import unittest

from tech_analysis.candlestick.pattern import is_hammer, is_inverted_hammer, \
    is_big_black_candle


class TestCandlestickPattern(unittest.TestCase):

    def test_is_bullish_hammer(self):
        candlestick = {'open': 5.1, 'close': 5.3, 'high': 5.35, 'low': 4.3}

        self.assertEqual(is_hammer(candlestick, t1=0.01, t2=0.05, t3=0.05), True)

    def test_is_bearish_hammer(self):
        candlestick = {'open': 5.3, 'close': 5.1, 'high': 5.35, 'low': 4.3}

        self.assertEqual(is_hammer(candlestick, t1=0.01, t2=0.05, t3=0.05), True)

    def test_is_bullish_inverted_hammer(self):
        candlestick = {'open': 5.1, 'close': 5.3, 'high': 5.9, 'low': 5.05}

        self.assertEqual(is_inverted_hammer(candlestick, t1=0.05, t2=0.05, t3=0.01), True)

    def test_is_bearish_inverted_hammer(self):
        candlestick = {'open': 5.3, 'close': 5.1, 'high': 5.9, 'low': 5.05}

        self.assertEqual(is_inverted_hammer(candlestick, t1=0.05, t2=0.05, t3=0.01), True)

    def test_is_big_black_candle(self):
        candlestick = {'open': 5.0, 'close': 4.2, 'high': 5.02, 'low': 4.18}

        self.assertEqual(is_big_black_candle(candlestick, t1=0.01, t2=0.05, t3=0.01), True)


if __name__ == '__main__':
    unittest.main()
