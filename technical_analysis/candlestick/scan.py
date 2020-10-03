"""
    Scan candlestick patterns.
"""

from technical_analysis.candlestick.signal import is_hammer_signal, is_inverted_hammer_signal


def scan_hammer(df, window_size=5, abs_slope=0.5, t1=4, t3=2, small_body=0.01):
    n = len(df)
    eval_dict = dict()
    for x in range(window_size, n):
        candlesticks = df.iloc[x - window_size:x].to_dict(orient="records")
        present_candlestick = candlesticks[-1]
        if is_hammer_signal(candlesticks, abs_slope, t1, t3, small_body):
            eval_dict[present_candlestick["date"]] = df.iloc[x - window_size:x + window_size]

    print("There are a total of {n} bullish patterns.".format(n=len(eval_dict)))

    return eval_dict


def scan_inverted_hammer(df, window_size=5, abs_slope=0.5, t1=2, t3=4, small_body=0.01):
    n = len(df)
    eval_dict = dict()
    for x in range(window_size, n):
        candlesticks = df.iloc[x - window_size:x].to_dict(orient="records")
        present_candlestick = candlesticks[-1]
        if is_inverted_hammer_signal(candlesticks, abs_slope, t1, t3, small_body):
            eval_dict[present_candlestick["date"]] = df.iloc[x - window_size:x + window_size]

    print("There are a total of {n} bullish patterns.".format(n=len(eval_dict)))

    return eval_dict

# def scan_dragonfly_doji_reversal(df, window_size=3, long_lower_shadow=0.02):
#     eval_dict = dict()
#     for x in range(window_size, len(df)):
#         candlesticks = df.iloc[x - window_size:x].to_dict(orient="records")
#         present_candlestick = candlesticks[-1]
#         if is_dragonfly_doji_reversal(candlesticks, long_lower_shadow=long_lower_shadow):
#             eval_dict[present_candlestick["date"]] = df.iloc[x - window_size:x + window_size]
#
#     print("There are a total of {n} reversals.".format(n=len(eval_dict)))
#
#     return eval_dict
#
#
# def scan_gravestone_doji_reversal(df, window_size=3, long_upper_shadow=0.02):
#     n = len(df)
#     eval_dict = dict()
#     for x in range(window_size, n):
#         candlesticks = df.iloc[x - window_size:x].to_dict(orient="records")
#         present_candlestick = candlesticks[-1]
#         if is_gravestone_doji_reversal(candlesticks, long_upper_shadow=long_upper_shadow):
#             eval_dict[present_candlestick["date"]] = df.iloc[x - window_size:x + window_size]
#
#     print("There are a total of {n} reversals.".format(n=len(eval_dict)))
#
#     return eval_dict

# if __name__ == "__main__":
#     # asx_stock_watchlist = ["tls.ax", "wbc.ax", "nov.ax", "cba.ax", "hack.ax", "ltr.ax"]
#
#     # plot_candlestick("tls.ax")
#     stock_path = "data/asx_stock/csv"
#
#     wbc = "wbc.ax"
#     # df = pd.read_csv(os.path.join(stock_path, wbc, "hist_price_19880128_20200921.csv"))
#     # scan_hammer(df, window_size=5)
#     # scan_inverted_hammer(df, window_size=5)
#     # scan_dragonfly_doji(df, window_size=3)
#
#     tls = "tls.ax"
#     df = pd.read_csv(os.path.join(stock_path, tls, "hist_price_19971127_20200921.csv"))
#     # scan_hammer(df, window_size=7)
#     # scan_inverted_hammer(df, window_size=5)
#     scan_reversal_dragonfly_doji(df, window_size=7)
