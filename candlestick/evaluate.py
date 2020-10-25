import pandas as pd
import plotly.graph_objects as go

from candlestick.core.trend import is_bullish_or_bearish_trend


# util functions.
def plot_candlestick(price_df):
    fig = go.Figure(data=[go.Candlestick(
        x=price_df['date'],
        open=price_df['open'],
        high=price_df['high'],
        low=price_df['low'],
        close=price_df['close'])])

    fig.show()


def debug(window_df):
    while True:
        date = input("Type the date to plot its neighbouring candlesticks: \n")
        window = window_df.loc[window_df["date"] == date]

        candlesticks = [*window['his'].values[0], window['cur'].values[0], *window['fut'].values[0]]
        plot_candlestick(pd.DataFrame(candlesticks))


# evaluate functions.
def evaluate_higher_price(price_df, date_or_index, fut_size, key, a_share):
    """"
        Evaluate whether there is any higher price than the trade day, according to future fut_size trade days. Key
        can be high, low, open or close.

        {"date": "2020-10-10", "fut_size": 3, "key": "close", "a_share": False}

        # bullish_days:             number of future trade days those have a higher price.
        # highest_price:            highest price occurred in future trade days.
        # highest_growth:           highest growth rate.
        # bullish_trend:            whether a bullish tread is present in future trade days.
    """
    # Ensure the price_df is sorted in ascending order according to date.
    price_df = price_df.sort_values(by="date", axis='index', ascending=True) \
        .reset_index().drop(labels="index", axis="columns")

    # By default, it evaluates the first candlestick in the price_df.
    index = 0
    if date_or_index:
        # Index.
        if type(date_or_index) == int:
            index = date_or_index
            if index < 0 or index > len(price_df) - 1:
                return None
        # Date.
        if type(date_or_index) == str:
            index = price_df.index[price_df["date"] == date_or_index]
            if len(index) > 0:
                index = index[0]
            else:
                return None

    date = price_df.iloc[index]["date"]
    stock_code = price_df.iloc[index]["ticker"]

    if index + fut_size > len(price_df):
        print("{stock_code} does not have {fut_size} future candlesticks."
              .format(fut_size=fut_size, stock_code=stock_code))
        return None

    price = price_df.iloc[index]["close"]
    if a_share:
        fut_price_df = price_df.iloc[index + 1:index + fut_size - 1]
    else:
        fut_price_df = price_df.iloc[index:index + fut_size]

    max_fut_price = round(fut_price_df[key].max(), 3)
    result = {
        "stock_code": stock_code,
        "date": date,
        "fut_size": fut_size,
        "key": key,
        "a_share": a_share,
        "bullish_days": fut_price_df[key].ge(price).sum(),
        "bullish_trend": is_bullish_or_bearish_trend(fut_price_df.to_dict(orient="records"), key=key),
        "highest_price": max_fut_price,
        "highest_percent": round(max_fut_price / price - 1, 3),
    }

    return result


def evaluate_bullish_trend(price_df, date_or_index, fut_size, key, a_share):
    pass


def evaluate_higher_price_all(price_df, fut_size, key, a_share):
    """"
        Evaluate all the dates/indexes across the price_df using evaluate_higher_price.
        Key can be high, low, open or close.

        {"fut_size": 3, "key": "close", "a_share": False}

    """
    n = len(price_df)
    result_df = pd.DataFrame([evaluate_higher_price(price_df, t, fut_size, key, a_share) for t in range(n - fut_size)])

    print(result_df)
    result = {
        "stock_code": result_df.iloc[0]["stock_code"],
        "fut_size": result_df.iloc[0]["fut_size"],
        "key": result_df.iloc[0]["key"],
        "a_share": result_df.iloc[0]["a_share"],
        "trade_days": n - fut_size,
        "profitable_trade_days": ((result_df["highest_percent"] > 0) &
                                  (result_df["bullish_trend"] == "bullish")).value_counts()[True],
        "bullish_days_ratio": round(result_df["bullish_days"].mean() / result_df.iloc[0]["fut_size"], 3),
        "bullish_trend_ratio": round(result_df["bullish_trend"].value_counts()["bullish"] / n, 3),
        "highest_percent_avg": round(result_df["highest_percent"].mean(), 3)
    }

    return result


# TODO: it will be changed to support multiple scan funcs. 25/10/2020 MX
def evaluate_stock(price_df, scan_func, scan_func_params, eval_func, eval_func_params):
    """
        Evaluate how a stock performs against a candlestick pattern.

        scan_func_params:  ref_size, hammer_params, market_top_or_bottom_params, enhance
    """
    n = len(price_df)
    is_patterns = [scan_func(price_df, t, **scan_func_params) for t in range(n)]
    eval_results = [eval_func(price_df, t, **eval_func_params) for t in range(n)]

    print(is_patterns)
    print(eval_results)

    # windows_df = evaluate_any_higher_price(windows, key="high", a_share=True)
    # windows_df0 = windows_df.loc[windows_df["is_hammer_signal"]]
    #
    # n = len(windows_df)
    # n0 = len(windows_df0)
    #
    # rate = len(windows_df[windows_df["higher_fut_price"] >= 0]) / n
    # if n0 == 0:
    #     rate0 = 0
    # else:
    #     rate0 = len(windows_df0[windows_df0["higher_fut_price"] >= 0]) / n0
    #
    # # scale: billion
    # trade_scale = round(price_df.apply(lambda row: row["volume"] * row["close"], axis="columns").mean() / 1000000000, 3)
    #
    # result = {
    #     "stock_code": stock_code,
    #     "trade_scale": trade_scale,
    #     "trade_days": n,
    #     "n_hammer_signal": n0,
    #     "benchmark_success_rate": round(rate, 3),
    #     "success_rate": round(rate0, 3),
    #     "improvement": round(rate0 / rate - 1, 3),
    #     "method": "any_higher_high_price",
    #     **params_dict
    # }
    # return windows
