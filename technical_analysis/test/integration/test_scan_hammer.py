import os
import re

import pandas as pd

from technical_analysis.candlestick.scan import scan, scan_hammer
from technical_analysis.candlestick.trend import evaluate


def test_stock(stock_code, stock_params, stock_path="data/asx_stock/csv"):
    stock_path = os.path.join(stock_path, stock_code)
    filenames = os.listdir(stock_path)

    price_filename = [filename for filename in filenames if re.match(r"hist_price", filename)]
    # TODO it should choose the latest hist_price if there are multiple filenames.
    stock_path = os.path.join(stock_path, price_filename[0])

    df = pd.read_csv(stock_path)

    benchmark_eval_dict = scan(df, window_size=stock_params["window_size"])
    benchmark_success_rate = evaluate(benchmark_eval_dict, print_detail=False)
    eval_dict = scan_hammer(df, **stock_params)
    success_rate = evaluate(eval_dict, print_detail=False)

    improvement = success_rate / benchmark_success_rate - 1

    print("The improvement is {improvement}, from {rate1} to {rate2}".format(improvement=round(improvement, 2),
                                                                             rate1=benchmark_success_rate,
                                                                             rate2=success_rate))

    # debug
    # while True:
    #     date = input("Type the date to plot its neighbouring candlesticks: \n")
    #     plot_candlestick(eval_dict[date])

    # pd.set_option('max_columns', None)
    # print(eval_dict[date])

    return success_rate - benchmark_success_rate, success_rate


# def test_stocks(stock_code, default_stock_params, stock_params=None):
#     pass


if __name__ == "__main__":
    # wbc_params_dict = {
    #     "window_size": 5,
    #     "abs_slope": 0.2,
    #     "t1": 2,
    #     "t3": 1,
    #     "small_body": 0.1,
    # }

    params_dict = {
        "window_size": 5,
        "abs_slope": 0,
        "t1": 1,
        "t3": 1,
        "small_body": 0.1,
    }

    sz_stocks = ["300655.SZ", "300122.SZ", "002007.SZ", "300185.SZ", "002594.SZ", "002625.SZ", "000625.SZ",
                 "300750.SZ", "000333.SZ", "002475.SZ", "000725.SZ", "300730.SZ", "002230.SZ", "000002.SZ", "002285.SZ",
                 "000656.SZ", "000011.SZ", "000069.SZ", "000006.SZ", "300369.SZ"]

    improvements = list()
    success_rates = list()
    for sz_stock in sz_stocks:
        improvement, success_rate = test_stock(sz_stock, params_dict, "data/sz_stock/csv")
        print(improvement)
        print(success_rate)
        improvements.append(improvement)
        success_rates.append(success_rate)

    print(sum(improvements) / len(improvements))
    print(sum(success_rates) / len(success_rates))
