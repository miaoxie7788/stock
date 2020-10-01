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


def is_bullish_or_bearish_trend(candlesticks, key="close"):
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
    if slope > 0:
        return "bullish"
    return "bearish"


# TODO: is_market_bottom and is_market_top can be combined into one.
def is_market_bottom(candlesticks, key="low"):
    """
        A couple of consecutive daily prices (by default low prices) present a bearish_trend.
        If the latest daily price is minimal, it is a market bottom; otherwise not.
    """
    present_candlestick = candlesticks[-1]
    history_candlesticks = candlesticks[:-1]

    if is_bullish_or_bearish_trend(history_candlesticks) == "bearish":
        present_price = present_candlestick[key]
        history_prices = [candlestick[key] for candlestick in history_candlesticks if not np.isnan(candlestick[key])]

        if present_price <= min(history_prices):
            return True

    return False


def is_market_top(candlesticks, key="high"):
    """
        A couple of consecutive daily prices (by default high prices) present a bullish_trend.
        If the latest daily price is maximal, it is a market top; otherwise not.
    """
    present_candlestick = candlesticks[-1]
    history_candlesticks = candlesticks[:-1]

    if is_bullish_or_bearish_trend(history_candlesticks) == "bullish":
        present_price = present_candlestick[key]
        history_prices = [candlestick[key] for candlestick in history_candlesticks if not np.isnan(candlestick[key])]

        if present_price >= max(history_prices):
            return True

    return False


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
