import unittest

import pandas as pd

from candlestick.evaluate import evaluate_higher_price, evaluate_higher_price_all

pd.set_option('display.max_columns', None)

#       date     open  high  low    close   adjclose volume    ticker
# 0  2020-10-21  9.58  9.70  9.51   9.70      9.70  61622129  600000.SS
# 1  2020-10-20  9.63  9.65  9.51   9.58      9.58  46687029  600000.SS
# 2  2020-10-19  9.73  9.93  9.64   9.65      9.65  84532385  600000.SS
# 3  2020-10-16  9.61  9.77  9.60   9.72      9.72  74850236  600000.SS
# 4  2020-10-15  9.54  9.72  9.53   9.62      9.62  66146732  600000.SS
# 5  2020-10-14  9.54  9.56  9.50   9.53      9.53  42969217  600000.SS
# 6  2020-10-13  9.58  9.58  9.52   9.54      9.54  28059097  600000.SS
# 7  2020-10-12  9.45  9.63  9.42   9.59      9.59  66671637  600000.SS
# 8  2020-10-09  9.44  9.48  9.40   9.42      9.42  39772687  600000.SS

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

    def test_evaluate_higher_price_all(self):
        params = {'fut_size': 3,
                  'key': 'high',
                  'a_share': False, }

        result = evaluate_higher_price_all(price_df, **params)
        print(result)
        self.assertIsInstance(result, dict)

    # def test_evaluate_stock(self):
    #     # ax_tls_price_19971127_20201014.csv
    #
    #     filename = "data/stock/ax_wbc_price_19880128_20201014.csv"
    #     price_df = pd.read_csv(filename)
    #
    #     scan_bullish_hammer_params = {
    #         "hammer_params": {"t1": 1,
    #                           "t3": 2,
    #                           "small_body": 0.1},
    #         "market_top_or_bottom_params": {"key": "low",
    #                                         "abs_slope": 0.05},
    #
    #         "enhanced": True,
    #         "ref_size": 5,
    #         # "date_or_index": None
    #     }
    #
    #     evaluate_higher_price_params = {
    #         "fut_size": 3,
    #         # "date_or_index": None,
    #         "key": "high",
    #         "a_share": False
    #     }
    #
    #     evaluate_stock(price_df,
    #                    scan_func=scan_bullish_hammer,
    #                    scan_func_params=scan_bullish_hammer_params,
    #                    eval_func=evaluate_higher_price,
    #                    eval_func_params=evaluate_higher_price_params)


if __name__ == '__main__':
    unittest.main()
