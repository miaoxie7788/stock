"""
    Scan candlestick patterns.
"""

from candlestick.core.signal import is_hammer_signal, is_inverted_hammer_signal


def scan_benchmark(df, window_size):
    """
        Benchmark.
    """
    n = len(df)
    eval_dict = dict()
    for x in range(window_size, n - window_size + 1):
        eval_dict[df.iloc[x]["date"]] = df.iloc[x - window_size:x + window_size]

    # print("There are a total of {n} benchmark patterns.".format(n=len(eval_dict)))

    return eval_dict


def scan_hammer(df, window_size, abs_slope, t1, t3, small_body):
    n = len(df)
    eval_dict = dict()
    for x in range(window_size, n - window_size + 1):
        candlesticks = df.iloc[x - window_size:x + 1].to_dict(orient="records")
        present_candlestick = candlesticks[-1]
        if is_hammer_signal(candlesticks, abs_slope, t1, t3, small_body):
            eval_dict[present_candlestick["date"]] = df.iloc[x - window_size:x + window_size]

    # print("There are a total of {n} bullish patterns.".format(n=len(eval_dict)))

    return eval_dict


def scan_inverted_hammer(df, window_size, abs_slope, t1, t3, small_body):
    n = len(df)
    eval_dict = dict()
    for x in range(window_size, n - window_size + 1):
        candlesticks = df.iloc[x - window_size:x + 1].to_dict(orient="records")
        present_candlestick = candlesticks[-1]
        if is_inverted_hammer_signal(candlesticks, abs_slope, t1, t3, small_body):
            eval_dict[present_candlestick["date"]] = df.iloc[x - window_size:x + window_size]

    # print("There are a total of {n} bullish patterns.".format(n=len(eval_dict)))

    return eval_dict
