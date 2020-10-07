"""
    Scan candlestick patterns.
"""

from candlestick.core.signal import is_hammer_signal, is_inverted_hammer_signal


def scan_hammer(candlestick_df, his_size, fut_size, abs_slope, t1, t3, small_body, enhanced):
    n = len(candlestick_df)
    windows = list()
    for t in range(his_size, n - fut_size):
        his_candlesticks = candlestick_df.iloc[t - his_size: t].to_dict(orient="records")
        cur_candlestick = candlestick_df.iloc[t].to_dict()
        fut_candlesticks = candlestick_df.iloc[t + 1: t + fut_size + 1].to_dict(orient="records")

        if is_hammer_signal(cur_candlestick, his_candlesticks, abs_slope, t1, t3, small_body, enhanced):
            signal = True
        else:
            signal = False

        window = {"date": cur_candlestick["date"], "cur": cur_candlestick, "his": his_candlesticks,
                  "fut": fut_candlesticks, "is_hammer_signal": signal}

        windows.append(window)

    return windows


def scan_inverted_hammer(candlestick_df, his_size, fut_size, abs_slope, t1, t3, small_body, enhanced):
    n = len(candlestick_df)
    windows = list()
    for t in range(his_size, n - fut_size):
        his_candlesticks = candlestick_df.iloc[t - his_size: t].to_dict(orient="records")
        cur_candlestick = candlestick_df.iloc[t].to_dict()
        fut_candlesticks = candlestick_df.iloc[t + 1: t + fut_size + 1].to_dict(orient="records")

        if is_inverted_hammer_signal(cur_candlestick, his_candlesticks, abs_slope, t1, t3, small_body, enhanced):
            signal = True
        else:
            signal = False

        window = {"date": cur_candlestick["date"], "cur": cur_candlestick, "his": his_candlesticks,
                  "fut": fut_candlesticks, "is_inverted_hammer_signal": signal}

        windows.append(window)

    return windows
