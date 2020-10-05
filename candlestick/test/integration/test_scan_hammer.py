import os
import re

import pandas as pd

from candlestick import evaluate
from candlestick import scan_benchmark, scan_hammer


def test_stock(stock_code, stock_params, path="data/asx_stock/csv"):
    print("Testing {stock_code}".format(stock_code=stock_code))
    stock_path = os.path.join(path, stock_code)
    filenames = os.listdir(stock_path)
    price_filename = os.path.join(stock_path,
                                  [filename for filename in filenames
                                   if re.match(r"hist_price_\d{8}_\d{8}.csv", filename)][0])

    df = pd.read_csv(price_filename)

    benchmark_eval_dict = scan_benchmark(df, window_size=stock_params["window_size"])
    benchmark_success_rate = evaluate(benchmark_eval_dict, print_detail=False)

    eval_dict = scan_hammer(df, **stock_params)
    success_rate = evaluate(eval_dict, print_detail=False)

    # scale: billion
    trade_scale = round(df.apply(lambda row: row["volume"] * row["close"], axis="columns").mean() / 1000000000, 3)

    result = {
        "stock_code": stock_code,
        "n_trade_days": len(df),
        "n_hammer": len(eval_dict),
        "benchmark_success_rate": round(benchmark_success_rate, 3),
        "success_rate": round(success_rate, 3),
        "trade_scale": trade_scale,
        "improvement": round(success_rate / benchmark_success_rate - 1, 3),
        **params_dict
    }

    # debug
    # while True:
    #     date = input("Type the date to plot its neighbouring candlesticks: \n")
    #     plot_candlestick(eval_dict[date])

    # pd.set_option('max_columns', None)
    # print(eval_dict[date])

    return result


if __name__ == "__main__":
    # params_dict = {
    #     "window_size": 5,
    #     "abs_slope": 0.1,
    #     "t1": 1,
    #     "t3": 1,
    #     "small_body": 0.1,
    # }
    #
    # sz_stocks = ["300655.SZ", "300122.SZ", "002007.SZ", "300185.SZ", "002594.SZ", "002625.SZ",
    #              "000625.SZ", "300750.SZ", "000333.SZ", "002475.SZ", "000725.SZ", "300730.SZ", "002230.SZ",
    #              "000002.SZ", "002285.SZ", "000656.SZ", "000011.SZ", "000069.SZ", "000006.SZ", "300369.SZ"]
    #
    #
    # result_df = pd.DataFrame([test_stock(stock, params_dict, "data/sz_stock/csv") for stock in sz_stocks])
    #

    asx_stocks = ["abp.ax", "apt.ax", "boq.ax", "bpt.ax", "ctx.ax", "car.ax", "csl.ax", "dhg.ax", "dmp.ax", "fph.ax",
                  "gem.ax", "hvn.ax", "ire.ax", "jbh.ax", "mgr.ax", "mpl.ax", "tls.ax", "wbc.ax", "orh.ax", "cba.ax", ]

    params_dict = {
        "window_size": 5,
        "abs_slope": 0.05,
        "t1": 1,
        "t3": 2,
        "small_body": 0.1,
    }

    result_df = pd.DataFrame([test_stock(stock, params_dict, "data/asx_stock/csv") for stock in asx_stocks])
    result_df.to_csv("asx_scan_hammer_results3.csv", index=False, header=True)
