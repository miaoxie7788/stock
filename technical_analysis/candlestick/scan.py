"""
    Scan candlestick patterns.
"""

from technical_analysis.candlestick.pattern import is_bullish_or_bearish_trend, is_dragonfly_doji_reversal, \
    is_gravestone_doji_reversal


def scan_dragonfly_doji_reversal(df, window_size=3, long_lower_shadow=0.02):
    n = len(df)
    reversal_dict = dict()
    for x in range(window_size, n):
        candlesticks = df.iloc[x - window_size:x].to_dict(orient="records")
        present_candlestick = candlesticks[-1]
        if is_dragonfly_doji_reversal(candlesticks, long_lower_shadow=long_lower_shadow):
            reversal_dict[present_candlestick["date"]] = df.iloc[x - window_size:x + window_size]

    n = len(reversal_dict)
    print("There are a total of {n} reversals.".format(n=n))

    return reversal_dict


def scan_gravestone_doji_reversal(df, window_size=3, long_upper_shadow=0.02):
    n = len(df)
    reversal_dict = dict()
    for x in range(window_size, n):
        candlesticks = df.iloc[x - window_size:x].to_dict(orient="records")
        present_candlestick = candlesticks[-1]
        if is_gravestone_doji_reversal(candlesticks, long_upper_shadow=long_upper_shadow):
            reversal_dict[present_candlestick["date"]] = df.iloc[x - window_size:x + window_size]

    n = len(reversal_dict)
    print("There are a total of {n} reversals.".format(n=n))

    return reversal_dict


def scan_hammer_reversal(df, window_size=5):
    def parameterised_is_hammer(candlestick):
        return is_hammer(candlestick, t1=4, t3=2, small_body=0.01)

    df["is_hammer"] = df.apply(parameterised_is_hammer, axis="columns")
    neighbour_prices_dict = dict()
    for _, price in df[df.is_hammer].iterrows():
        x = price.name
        if x >= window_size:
            hist_prices = df.iloc[x - window_size:x + 1].to_dict(orient="records")
            if is_bullish_or_bearish_trend(hist_prices) == "bearish":
                # print("A bullish trend reversal is signaled on {date}".format(date=price["date"]))
                neighbour_prices_dict[price["date"]] = df.iloc[x - window_size:x + window_size]

    n = len(neighbour_prices_dict)
    print("There are a total of {n} reversals.".format(n=n))


def evaluate(reversal_dict, window_size=3):
    effective = 0
    for date, candlesticks in reversal_dict.items():
        future_candlesticks = candlesticks.iloc[window_size:].to_dict(orient="records")

        if is_bullish_or_bearish_trend(future_candlesticks) == "bullish":
            effective += 1
            print("It is effective on {date}".format(date=date))
        else:
            print("It is not effective on {date}".format(date=date))
    if len(reversal_dict) != 0:
        print("The successful rate is: {rate}".format(rate=effective / len(reversal_dict)))

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
