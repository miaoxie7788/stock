import pandas as pd
import plotly.graph_objects as go

from candlestick.core.trend import is_bullish_or_bearish_trend
from candlestick.scan import scan_bullish_hammer


# util functions.
def plot_candlestick(price_df):
    fig = go.Figure(data=[go.Candlestick(
        x=price_df['date'],
        open=price_df['open'],
        high=price_df['high'],
        low=price_df['low'],
        close=price_df['close'])])

    fig.show()


# def debug(price_df):
#     while True:
#         date = input("Type the date to plot its neighbouring candlesticks: \n")
#         window = price_df.loc[price_df["date"] == date]
#
#         candlesticks = [*window['his'].values[0], window['cur'].values[0], *window['fut'].values[0]]
#         plot_candlestick(pd.DataFrame(candlesticks))


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


def evaluate_higher_price_and_bullish_hammer(price_df, date_or_index, bullish_hammer_params, higher_price_params):
    bullish_hammer_pattern = scan_bullish_hammer(price_df, date_or_index, **bullish_hammer_params)
    result = evaluate_higher_price(price_df, date_or_index, **higher_price_params)
    if bullish_hammer_pattern:
        result["is_bullish_hammer"] = True
    else:
        result["is_bullish_hammer"] = False

    return result


def evaluate_higher_price_and_bullish_hammer_stock(price_df, bullish_hammer_params, higher_price_params):
    """"
        Evaluate all the dates/indexes across the price_df for a stock using evaluate_higher_price against
        bullish_hammer.
    """
    n = len(price_df)
    ref_size = bullish_hammer_params["ref_size"]
    fut_size = higher_price_params["fut_size"]
    result_df = pd.DataFrame([evaluate_higher_price_and_bullish_hammer(price_df, t,
                                                                       higher_price_params=higher_price_params,
                                                                       bullish_hammer_params=bullish_hammer_params)
                              for t in range(ref_size, n - fut_size)])

    bullish_hammer_df = result_df[result_df["is_bullish_hammer"]]

    result = {
        "stock_code": result_df.iloc[0]["stock_code"],
        "trade_days": n - fut_size - ref_size,
        "any_higher": round((result_df["highest_percent"] > 0).value_counts()[True] / len(result_df), 3),
        "bullish_trend": round(result_df["bullish_trend"].value_counts()["bullish"] / len(result_df), 3),
        "highest_percent_avg": round(result_df["highest_percent"].mean(), 3),
        "bullish_hammer_trade_days": len(bullish_hammer_df),
        "bullish_hammer_any_higher": round(
            (bullish_hammer_df["highest_percent"] > 0).value_counts()[True] / len(bullish_hammer_df), 3),
        "bullish_hammer_bullish_trend": round(
            bullish_hammer_df["bullish_trend"].value_counts()["bullish"] / len(bullish_hammer_df), 3),
        "bullish_hammer_highest_percent_avg": round(bullish_hammer_df["highest_percent"].mean(), 3),
        "bullish_hammer_params": bullish_hammer_params,
        "higher_price_params": higher_price_params,
    }

    return result
