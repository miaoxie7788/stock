import os

import pandas as pd

from technical_analysis.candlestick.plot import plot_candlestick
from technical_analysis.candlestick.scan import scan, scan_inverted_hammer
from technical_analysis.candlestick.trend import evaluate

if __name__ == "__main__":
    stock_path = "data/asx_stock/csv"

    # wbc_df = pd.read_csv(os.path.join(stock_path, "wbc.ax", "hist_price_19880128_20200921.csv"))
    # benchmark_eval_dict = scan(wbc_df, window_size=5)
    # evaluate(benchmark_eval_dict, print_detail=False)
    # eval_dict = scan_inverted_hammer(wbc_df, window_size=5, abs_slope=0.2, t1=1, t3=1, small_body=0.1)
    # evaluate(eval_dict)

    # tls_df = pd.read_csv(os.path.join(stock_path, "tls.ax", "hist_price_19971127_20200921.csv"))
    # benchmark_eval_dict = scan(tls_df, window_size=5)
    # evaluate(benchmark_eval_dict, print_detail=False)
    # eval_dict = scan_inverted_hammer(tls_df, window_size=5, abs_slope=0.05, t1=1, t3=1, small_body=0.1)
    # evaluate(eval_dict)

    # nov_df = pd.read_csv(os.path.join(stock_path, "nov.ax", "hist_price_20160117_20200921.csv"))
    # benchmark_eval_dict = scan(nov_df, window_size=5)
    # evaluate(benchmark_eval_dict, print_detail=False)
    # eval_dict = scan_inverted_hammer(nov_df, window_size=5, abs_slope=0.0, t1=1, t3=1, small_body=0.2)
    # evaluate(eval_dict)

    sz_df = pd.read_csv(os.path.join(stock_path, "300369.SZ", "hist_price_20140129_20200926.csv"))
    benchmark_eval_dict = scan(sz_df, window_size=5)
    evaluate(benchmark_eval_dict, print_detail=False)
    eval_dict = scan_inverted_hammer(sz_df, window_size=5, abs_slope=0.05, t1=1, t3=1, small_body=0.1)
    evaluate(eval_dict)

    while True:
        date = input("Type the date to plot its neighbouring candlesticks: \n")
        plot_candlestick(eval_dict[date])
