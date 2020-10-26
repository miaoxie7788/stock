import pandas as pd

pd.set_option('display.max_columns', None)


def evaluate_higher_price_and_bullish_hammer(price_df, date_or_index, bullish_hammer_params, higher_price_params):
    bullish_hammer_pattern = scan_bullish_hammer(price_df, date_or_index, **bullish_hammer_params)
    result = evaluate_higher_price(price_df, date_or_index, **higher_price_params)
    if bullish_hammer_pattern:
        result["is_bullish_hammer"] = True
    else:
        result["is_bullish_hammer"] = False

    return result


def evaluate_higher_price_and_bullish_hammer_stock(price_df, bullish_hammer_params, higher_price_params):
    """"
        Evaluate all the dates/indexes across the price_df for a stock using evaluate_higher_price against
        bullish_hammer.
    """
    n = len(price_df)
    ref_size = bullish_hammer_params["ref_size"]
    fut_size = higher_price_params["fut_size"]
    result_df = pd.DataFrame([evaluate_higher_price_and_bullish_hammer(price_df, t,
                                                                       higher_price_params=higher_price_params,
                                                                       bullish_hammer_params=bullish_hammer_params)
                              for t in range(ref_size, n - fut_size)])

    bullish_hammer_df = result_df[result_df["is_bullish_hammer"]]

    result = {
        "stock_code": result_df.iloc[0]["stock_code"],
        "trade_days": len(result_df),
        "any_higher": round((result_df["highest_percent"] > 0).value_counts()[True] / len(result_df), 3),
        "bullish_trend": round(result_df["bullish_trend"].value_counts()["bullish"] / len(result_df), 3),
        "highest_percent_avg": round(result_df["highest_percent"].mean(), 3),
        "bullish_hammer_trade_days": len(bullish_hammer_df),
        "bullish_hammer_any_higher": round(
            (bullish_hammer_df["highest_percent"] > 0).value_counts()[True] / len(bullish_hammer_df), 3),
        "bullish_hammer_bullish_trend": round(
            bullish_hammer_df["bullish_trend"].value_counts()["bullish"] / len(bullish_hammer_df), 3),
        "bullish_hammer_highest_percent_avg": round(bullish_hammer_df["highest_percent"].mean(), 3),
        "bullish_hammer_params": bullish_hammer_params,
        "higher_price_params": higher_price_params,
    }

    return result


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


if __name__ == "__main__":
    # asx_stocks = ["abp.ax", "apt.ax", "boq.ax", "bpt.ax", "ctx.ax", "car.ax", "csl.ax", "dhg.ax", "dmp.ax", "fph.ax",
    #               "gem.ax", "hvn.ax", "ire.ax", "jbh.ax", "mgr.ax", "mpl.ax", "tls.ax", "wbc.ax", "orh.ax", "cba.ax", ]
    #
    # params_dict = {
    #     "his_size": 5,
    #     "fut_size": 2,
    #     "abs_slope": 0.01,
    #     "t1": 1,
    #     "t3": 1.5,
    #     "small_body": 0.1,
    #     "enhanced": True
    # }
    #
    # # asx_stocks = ["apt.ax"]
    #
    # result_df = pd.DataFrame([test_stock(stock, params_dict, "data/asx_stock/csv") for stock in asx_stocks])
    # result_df.to_csv("asx_scan_hammer_results2.csv", index=False, header=True)

    with open("data/hs_stock_codes") as f:
        hs_stocks = [stock.strip() for stock in f.readlines()]

    hs_params = {
        "bullish_hammer_params": {
            "hammer_params": {"t1": 3,
                              "t3": 4,
                              "small_body": 0.05},
            "key": "low",
            "abs_slope": 0.25,
            "enhanced": True,
        },
        "ref_size": 5,
        "fut_size": 2,
    }
    # 600909.ss
    # 601878.ss
    # 688008.ss
    # 688018.ss
    # 300339.sz
    # 603368.ss     0.82        2%

    hs_stocks = ["000997.sz"]
    result_df = pd.DataFrame([test_stock(stock, hs_params, "data/stock") for stock in hs_stocks])
    # result_df.to_csv("hs_scan_hammer_results2.csv", index=False, header=True)
