import os
import re

import pandas as pd

from candlestick.evaluate import evaluate_any_higher_price, scan_inverted_hammer

pd.set_option('display.max_columns', None)


def test_stock(stock_code, stock_params, path="data/asx_stock/csv"):
    # print("Testing {stock_code}".format(stock_code=stock_code))
    stock_path = os.path.join(path, stock_code)
    filenames = os.listdir(stock_path)
    stock_price_filename = os.path.join(stock_path,
                                        [filename for filename in filenames
                                         if re.match(r"hist_price_\d{8}_\d{8}.csv", filename)][0])

    stock_df = pd.read_csv(stock_price_filename)

    windows = scan_inverted_hammer(stock_df, **stock_params)

    windows_df = evaluate_any_higher_price(windows, key="open")
    windows_df0 = windows_df.loc[windows_df["is_inverted_hammer_signal"]]

    n = len(windows_df)
    n0 = len(windows_df0)

    rate = len(windows_df[windows_df["higher_fut_price"] >= 0]) / n
    if n0 == 0:
        rate0 = 0
    else:
        rate0 = len(windows_df0[windows_df0["higher_fut_price"] >= 0]) / n0

    # scale: billion
    trade_scale = round(stock_df.apply(lambda row: row["volume"] * row["close"], axis="columns").mean() / 1000000000, 3)

    result = {
        "stock_code": stock_code,
        "trade_scale": trade_scale,
        "trade_days": n,
        "n_hammer_signal": n0,
        "benchmark_success_rate": round(rate, 3),
        "success_rate": round(rate0, 3),
        "improvement": round(rate0 / rate - 1, 3),
        "method": "any_higher_open_price",
        **params_dict
    }

    print(result)
    # print(windows_df0[["date", "higher_fut_price"]])
    # debug(windows_df0)
    return result


if __name__ == "__main__":
    # asx_stocks = ["abp.ax", "apt.ax", "boq.ax", "bpt.ax", "ctx.ax", "car.ax", "csl.ax", "dhg.ax", "dmp.ax", "fph.ax",
    #               "gem.ax", "hvn.ax", "ire.ax", "jbh.ax", "mgr.ax", "mpl.ax", "tls.ax", "wbc.ax", "orh.ax", "cba.ax", ]
    #
    # params_dict = {
    #     "his_size": 5,
    #     "fut_size": 3,
    #     "abs_slope": 0.01,
    #     "t1": 2,
    #     "t3": 1,
    #     "small_body": 0.1,
    #     "enhanced": False
    # }
    #
    # # asx_stocks = ["cba.ax"]
    #
    # result_df = pd.DataFrame([test_stock(stock, params_dict, "data/asx_stock/csv") for stock in asx_stocks])
    # result_df.to_csv("asx_scan_inverted_hammer_results5.csv", index=False, header=True)

    with open("data/hs_stock_codes_1_800") as f:
        hs_stocks = [stock.strip() for stock in f.readlines()]

    params_dict = {
        "his_size": 5,
        "fut_size": 3,
        "abs_slope": 0.01,
        "t1": 2,
        "t3": 1,
        "small_body": 0.1,
        "enhanced": True,
    }
    result_df = pd.DataFrame([test_stock(stock, params_dict, "data/hs_stock/csv") for stock in hs_stocks])
    result_df.to_csv("hs_scan_inverted_hammer_results3.csv", index=False, header=True)
