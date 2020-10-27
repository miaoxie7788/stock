"""
    This is to test scan_bullish_hammer and how to select the parameters for asx and hs respectively.
"""

import os

import pandas as pd

from candlestick.evaluate import evaluate_higher_price
from candlestick.scan import scan_bullish_hammer

pd.set_option('display.max_columns', None)


def scan_bullish_hammer_stock(price_df, bullish_hammer_params):
    n = len(price_df)
    patterns = [scan_bullish_hammer(price_df, t, **bullish_hammer_params) for t in range(n)]
    price_df["bullish_hammer"] = [True if pattern else False for pattern in patterns]

    return price_df


def evaluate_higher_price_stock(price_df, higher_price_params):
    n = len(price_df)

    if "bullish_hammer" not in price_df.columns:
        raise ValueError("The price_df has not scanned bullish_hammer.")

    fut_size = higher_price_params["fut_size"]
    result_df = pd.DataFrame([evaluate_higher_price(price_df, t, **higher_price_params) for t in range(n - fut_size)])
    bullish_hammer_df = result_df[price_df.iloc[:n - fut_size]["bullish_hammer"]]

    result = {
        "stock_code": result_df.iloc[0]["stock_code"],
        "trade_days": len(result_df),
        "any_higher": round(
            len(result_df[result_df["highest_percent"] > 0]) / len(result_df), 3),
        "bullish_trend": round(
            len(result_df[result_df["bullish_trend"] == "bullish"]) / len(result_df), 3),
        "highest_percent_avg": round(result_df["highest_percent"].mean(), 3),
        "bullish_hammer_trade_days": len(bullish_hammer_df),
        "bullish_hammer_any_higher": round(
            len(bullish_hammer_df[bullish_hammer_df["highest_percent"] > 0]) / len(bullish_hammer_df),
            3) if len(bullish_hammer_df) > 0 else 0,
        "bullish_hammer_bullish_trend": round(
            len(bullish_hammer_df[bullish_hammer_df["bullish_trend"] == "bullish"]) / len(bullish_hammer_df),
            3) if len(bullish_hammer_df) > 0 else 0,
        "bullish_hammer_highest_percent_avg": round(bullish_hammer_df["highest_percent"].mean(),
                                                    3) if len(bullish_hammer_df) > 0 else 0,
    }

    return result


if __name__ == "__main__":
    cba_bullish_hammer_params = {
        "hammer_params": {
            "t1": 1,
            "t3": 2,
            "small_body": 0.1
        },
        "market_top_or_bottom_params": {
            "key": "low",
            "abs_slope": 0.02
        },
        "enhanced": True,
        "ref_size": 5,
    }

    cba_higher_price_params = {
        'fut_size': 3,
        'a_share': False,
        'key': 'high',
    }

    # ax_cnu_price_20111122_20201014.csv
    # cba = pd.read_csv("data/stock/ax_cba_price_19910930_20201014.csv")
    # cba = pd.read_csv("data/stock/ax_cnu_price_20111122_20201014.csv")

    csvs = os.listdir("data/stock")

    results = []
    for csv in csvs:
        cba = pd.read_csv("data/stock/" + csv)
        cba = scan_bullish_hammer_stock(cba, cba_bullish_hammer_params)

        result = evaluate_higher_price_stock(cba, cba_higher_price_params)

        print(result)
        results.append(result)

    pd.DataFrame(results).to_csv("asx_result.csv")
