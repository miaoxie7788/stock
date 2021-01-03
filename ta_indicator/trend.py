"""
    Trend lines.
"""

import numpy as np


def is_upward_or_downward_trend(y):
    """
        A list of consecutive values (prices or volumes) are fitted with a 1st order linear model y = ax + b.
        If a > 0, the trend is upward otherwise downward.

    """

    n = len(y)
    if n < 2:
        raise ValueError("There are at least 2 values to determine a trend.")

    x = np.array(range(1, n + 1))
    y = np.array(y)

    slope, _ = list(np.polyfit(x, y, 1))
    degree = np.degrees(np.arctan(slope))

    if degree > 0:
        upward_or_downward = "upward"
    else:
        upward_or_downward = "downward"

    return upward_or_downward, degree


def is_market_top_or_bottom(trend_y, y):
    """
        A list of consecutive values (prices or volumes) present a upward or downward trend.
        The last value is maximal/minimal in terms of a list of consecutive values, it is a market top/bottom;
        otherwise None.

        For example, a list of "close" prices present a downward trend, the last "low" price is minial in terms of
        recent "low" prices, it is a bottom.
    """

    upward_or_downward, _ = is_upward_or_downward_trend(trend_y)

    top_or_bottom = None
    if upward_or_downward == "upward" and y[-1] >= max(y[:-1]):
        top_or_bottom = "top"

    if upward_or_downward == "downward" and y[-1] <= min(y[:-1]):
        top_or_bottom = "bottom"

    return top_or_bottom
