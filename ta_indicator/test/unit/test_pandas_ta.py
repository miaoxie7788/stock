import unittest

from ta_stock_market_data.yahoo import get_stock_historical_data

dfs = get_stock_historical_data("tls.ax", ["price"])
df = dfs['ax_tls_price.csv']


class TestPandasTa(unittest.TestCase):

    def test_rsi(self):
        rsi = df.ta.rsi(length=14)

        self.assertIsNotNone(rsi)

    def test_ema(self):
        ema = df.ta.ema(length=10)

        self.assertIsNotNone(ema)


if __name__ == '__main__':
    unittest.main()
