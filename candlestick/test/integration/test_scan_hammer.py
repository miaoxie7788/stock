import os
import re

import pandas as pd

from candlestick.evaluate import evaluate_any_higher_price, debug
from candlestick.scan import scan_hammer

pd.set_option('display.max_columns', None)


def test_stock(stock_code, stock_params, path="data/asx_stock/csv"):
    print("Testing {stock_code}".format(stock_code=stock_code))
    stock_path = os.path.join(path, stock_code)
    filenames = os.listdir(stock_path)
    stock_price_filename = os.path.join(stock_path,
                                        [filename for filename in filenames
                                         if re.match(r"hist_price_\d{8}_\d{8}.csv", filename)][0])

    stock_df = pd.read_csv(stock_price_filename)

    windows = scan_hammer(stock_df, **stock_params)

    windows_df = evaluate_any_higher_price(windows, key="high")
    windows_df0 = windows_df.loc[windows_df["is_hammer_signal"]]

    n = len(windows_df)
    n0 = len(windows_df0)

    rate = len(windows_df[windows_df["higher_fut_price"]]) / n
    if n0 == 0:
        rate0 = 0
    else:
        rate0 = len(windows_df0[windows_df0["higher_fut_price"]]) / n0

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
        "method": "any_higher_high_price",
        **params_dict
    }

    print(result)
    print(windows_df0[["date", "higher_fut_price"]])
    debug(windows_df0)

    return result


if __name__ == "__main__":
    params_dict = {
        "his_size": 5,
        "fut_size": 2,
        "abs_slope": 0.05,
        "t1": 1,
        "t3": 2,
        "small_body": 0.1,
        "enhanced": True,
    }

    # sz_stocks = ["300655.SZ", "300122.SZ", "002007.SZ", "300185.SZ", "002594.SZ", "002625.SZ",
    #              "000625.SZ", "300750.SZ", "000333.SZ", "002475.SZ", "000725.SZ", "300730.SZ", "002230.SZ",
    #              "000002.SZ", "002285.SZ", "000656.SZ", "000011.SZ", "000069.SZ", "000006.SZ", "300369.SZ"]

    sz_stocks = ["000598.SZ"]
    result_df = pd.DataFrame([test_stock(stock, params_dict, "data/sz_stock/csv") for stock in sz_stocks])
    # result_df.to_csv("sz_scan_hammer_results.csv", index=False, header=True)

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
