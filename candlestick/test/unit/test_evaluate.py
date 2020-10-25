import unittest

import pandas as pd

from candlestick.evaluate import evaluate_higher_price, evaluate_higher_price_and_bullish_hammer, \
    evaluate_higher_price_and_bullish_hammer_stock

pd.set_option('display.max_columns', None)

# 2006-05-17,45.553199768066406,45.602901458740234,45.08570098876953,45.35430145263672,20.38704490661621,1696232.0,CBA.AX
# 2006-05-18,44.95640182495117,45.05590057373047,44.55860137939453,44.95640182495117,20.208187103271484,3262814.0,CBA.AX
# 2006-05-19,44.87689971923828,45.254798889160156,44.74760055541992,44.74760055541992,20.114330291748047,2143012.0,CBA.AX
# 2006-05-22,44.707801818847656,44.97629928588867,44.608299255371094,44.608299255371094,20.051715850830078,2437418.0,CBA.AX
# 2006-05-23,44.409400939941406,44.69779968261719,44.250301361083984,44.309898376464844,19.91757583618164,2580791.0,CBA.AX
# 2006-05-24,44.35969924926758,44.409400939941406,43.4744987487793,43.9718017578125,19.765602111816406,5033266.0,CBA.AX
# 2006-05-25,43.91210174560547,44.111000061035156,43.61370086669922,43.752899169921875,19.667207717895508,2406252.0,CBA.AX
# 2006-05-26,44.160701751708984,44.20050048828125,43.68330001831055,44.160701751708984,19.850513458251953,3559876.0,CBA.AX
# 2006-05-29,44.26020050048828,44.54859924316406,44.160701751708984,44.28010177612305,19.904184341430664,1102159.0,CBA.AX
# 2006-05-30,44.20050048828125,44.240299224853516,43.951900482177734,44.03139877319336,19.79239273071289,1002761.0,CBA.AX
# 2006-05-31,43.762901306152344,43.842498779296875,42.94729995727539,42.94729995727539,19.305082321166992,3836593.0,CBA.AX
# 2006-06-01,43.30540084838867,43.64350128173828,43.12630081176758,43.64350128173828,19.61802864074707,1818934.0,CBA.AX
price_df = pd.read_csv("data/stock/ax_cba_price_19910930_20201014.csv")


class TestEvaluate(unittest.TestCase):

    def test_evaluate_higher_price(self):
        params = {'date_or_index': '2006-05-26',
                  'fut_size': 5,
                  'key': 'high',
                  'a_share': True, }

        result = evaluate_higher_price(price_df, **params)
        # print(result)
        self.assertIsInstance(result, dict)

    def test_evaluate_higher_price_against_bullish_hammer(self):
        bullish_hammer_params = {
            "hammer_params": {
                "t1": 1,
                "t3": 2,
                "small_body": 0.1},
            "market_top_or_bottom_params": {
                "key": "low",
                "abs_slope": 0.05},
            "enhanced": True,
            "ref_size": 5,
        }

        higher_price_params = {
            'fut_size': 3,
            'a_share': False,
            'key': 'high',
        }

        result = evaluate_higher_price_and_bullish_hammer(price_df,
                                                          "2006-05-26",
                                                          bullish_hammer_params=bullish_hammer_params,
                                                          higher_price_params=higher_price_params)
        # print(result)
        self.assertIsInstance(result, dict)

    def test_evaluate_stock_against_bullish_hammer(self):
        bullish_hammer_params = {
            "hammer_params": {
                "t1": 1,
                "t3": 2,
                "small_body": 0.1},
            "market_top_or_bottom_params": {
                "key": "low",
                "abs_slope": 0.02},
            "enhanced": True,
            "ref_size": 5,
        }

        higher_price_params = {
            'fut_size': 2,
            'a_share': False,
            'key': 'high',
        }

        result = evaluate_higher_price_and_bullish_hammer_stock(price_df,
                                                                bullish_hammer_params=bullish_hammer_params,
                                                                higher_price_params=higher_price_params)
        print(result)
        self.assertIsInstance(result, dict)


if __name__ == '__main__':
    unittest.main()
