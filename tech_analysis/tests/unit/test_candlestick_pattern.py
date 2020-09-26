import unittest

from tech_analysis.candlestick.pattern import is_hammer, is_inverted_hammer


class TestCandlestickPattern(unittest.TestCase):

    def test_is_hammer(self):
        price = {'open': 5.0, 'close': 5.3, 'high': 5.1, 'low': 4.3}

        self.assertEqual(is_hammer(price), True)

    def test_is_inverted_hammer(self):
        price = {'open': 5.0, 'close': 5.2, 'high': 5.8, 'low': 4.95}

        self.assertEqual(is_inverted_hammer(price), True)


if __name__ == '__main__':
    unittest.main()
