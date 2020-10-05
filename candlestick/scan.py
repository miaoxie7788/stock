"""
    Scan candlestick patterns.
"""

from candlestick.core.signal import is_hammer_signal, is_inverted_hammer_signal


def scan_hammer(df, his_size, fut_size, abs_slope, t1, t3, small_body):
    n = len(df)
    windows = list()
    for t in range(his_size, n - fut_size):
        his_candlesticks = df.iloc[t - his_size: t].to_dict(orient="records")
        cur_candlestick = df.iloc[t].to_dict()
        fut_candlesticks = df.iloc[t + 1: t + fut_size + 1].to_dict(orient="records")

        if is_hammer_signal(cur_candlestick, his_candlesticks, abs_slope, t1, t3, small_body):
            signal = True
        else:
            signal = False

        window = {"date": cur_candlestick["date"], "cur": cur_candlestick, "his": his_candlesticks,
                  "fut": fut_candlesticks, "signal": signal}

        windows.append(window)

    return windows


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
