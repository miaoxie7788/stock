import unittest

import pandas as pd

from ta_candlestick.evaluate import evaluate_higher_price

pd.set_option('display.max_columns', None)

price_df = pd.DataFrame([{'date': '2020-10-21',
                          'open': 9.579999923706056,
                          'high': 9.699999809265137,
                          'low': 9.510000228881836,
                          'close': 9.699999809265137,
                          'adjclose': 9.699999809265137,
                          'volume': 61622129,
                          'ticker': '600000.SS'},
                         {'date': '2020-10-20',
                          'open': 9.630000114440918,
                          'high': 9.649999618530273,
                          'low': 9.510000228881836,
                          'close': 9.579999923706056,
                          'adjclose': 9.579999923706056,
                          'volume': 46687029,
                          'ticker': '600000.SS'},
                         {'date': '2020-10-19',
                          'open': 9.729999542236328,
                          'high': 9.93000030517578,
                          'low': 9.640000343322754,
                          'close': 9.649999618530273,
                          'adjclose': 9.649999618530273,
                          'volume': 84532385,
                          'ticker': '600000.SS'},
                         {'date': '2020-10-16',
                          'open': 9.609999656677246,
                          'high': 9.770000457763672,
                          'low': 9.600000381469727,
                          'close': 9.720000267028807,
                          'adjclose': 9.720000267028807,
                          'volume': 74850236,
                          'ticker': '600000.SS'},
                         {'date': '2020-10-15',
                          'open': 9.539999961853027,
                          'high': 9.720000267028807,
                          'low': 9.529999732971193,
                          'close': 9.619999885559082,
                          'adjclose': 9.619999885559082,
                          'volume': 66146732,
                          'ticker': '600000.SS'},
                         {'date': '2020-10-14',
                          'open': 9.539999961853027,
                          'high': 9.5600004196167,
                          'low': 9.5,
                          'close': 9.529999732971193,
                          'adjclose': 9.529999732971193,
                          'volume': 42969217,
                          'ticker': '600000.SS'},
                         {'date': '2020-10-13',
                          'open': 9.579999923706056,
                          'high': 9.579999923706056,
                          'low': 9.520000457763672,
                          'close': 9.539999961853027,
                          'adjclose': 9.539999961853027,
                          'volume': 28059097,
                          'ticker': '600000.SS'},
                         {'date': '2020-10-12',
                          'open': 9.449999809265137,
                          'high': 9.630000114440918,
                          'low': 9.420000076293944,
                          'close': 9.59000015258789,
                          'adjclose': 9.59000015258789,
                          'volume': 66671637,
                          'ticker': '600000.SS'},
                         {'date': '2020-10-09',
                          'open': 9.4399995803833,
                          'high': 9.479999542236328,
                          'low': 9.399999618530273,
                          'close': 9.420000076293944,
                          'adjclose': 9.420000076293944,
                          'volume': 39772687,
                          'ticker': '600000.SS'}])


class TestEvaluate(unittest.TestCase):

    def test_evaluate_higher_price(self):
        params = {'date_or_index': '2020-10-12',
                  'fut_size': 5,
                  'key': 'high',
                  'a_share': True, }

        result = evaluate_higher_price(price_df, **params)
        # print(result)
        self.assertIsInstance(result, dict)


if __name__ == '__main__':
    unittest.main()
