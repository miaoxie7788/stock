import numpy as np


def extract_candlestick(candlestick):
    """
        Extract prices and price differences from a bullish or bearish candlestick.

        candlestick = {"open": y1, "close": y2, "high": y3, "low": y4}
    """
    y1, y2, y3, y4 = candlestick['open'], candlestick['close'], candlestick['high'], candlestick['low']

    if is_bullish_or_bearish_candlestick(candlestick) == "bullish":
        d1, d2, d3 = y3 - y2, y2 - y1, y1 - y4
    else:
        d1, d2, d3 = y3 - y1, y1 - y2, y2 - y4

    return y1, y2, y3, y4, d1, d2, d3


def is_bullish_or_bearish_candlestick(candlestick):
    if candlestick["close"] >= candlestick["open"]:
        return "bullish"
    return "bearish"


def is_bullish_or_bearish_trend(candlesticks, key="close", abs_slope=0):
    """
        A couple of consecutive daily prices (by default close prices) are fitted with a 1st order linear model y = ax
        + b. If a > 0, the trend is bullish otherwise bearish.
    """
    prices = [candlestick[key] for candlestick in candlesticks if not np.isnan(candlestick[key])]

    n = len(prices)
    if n <= 1:
        return None

    x = np.array(range(1, n + 1))
    y = np.array(prices)

    slope, _ = list(np.polyfit(x, y, 1))
    if slope > abs_slope:
        return "bullish"

    if slope < 0 and abs(slope) > abs_slope:
        return "bearish"

    return None


def is_market_top_or_bottom(candlesticks, key="low", abs_slope=0):
    """
        A couple of consecutive daily prices (by default low prices) present a bullish/bearish_trend.
        If the latest daily price is maximal/minimal, it is a market top/bottom; otherwise None.
    """
    present_candlestick = candlesticks[-1]
    history_candlesticks = candlesticks[:-1]

    present_price = present_candlestick[key]
    history_prices = [candlestick[key] for candlestick in history_candlesticks if not np.isnan(candlestick[key])]

    if is_bullish_or_bearish_trend(history_candlesticks, "close", abs_slope) == "bullish" \
            and present_price >= max(history_prices):
        return "top"

    if is_bullish_or_bearish_trend(history_candlesticks, "close", abs_slope) == "bearish" \
            and present_price <= min(history_prices):
        return "bottom"

    return None


def evaluate(eval_dict, window_size=3):
    effective = 0
    for date, candlesticks in eval_dict.items():
        future_candlesticks = candlesticks.iloc[window_size:].to_dict(orient="records")

        if is_bullish_or_bearish_trend(future_candlesticks) == "bullish":
            effective += 1
            print("It is effective on {date}".format(date=date))
        else:
            print("It is not effective on {date}".format(date=date))
    if len(eval_dict) != 0:
        print("The successful rate is: {rate}".format(rate=effective / len(eval_dict)))
