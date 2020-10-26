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
        Evaluate whether there is any price higher than the trade day given by date_or_index, according to future
        fut_size trade days. Key can be high, low, open or close.

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

    # TODO: decide to use "close" or key as default price of the first trade day. 26/10/2020
    # price = price_df.iloc[index]["close"]
    price = price_df.iloc[index][key]
    if a_share:
        fut_price_df = price_df.iloc[index + 2:index + fut_size + 1]
    else:
        fut_price_df = price_df.iloc[index + 1:index + fut_size + 1]

    max_fut_price = round(fut_price_df[key].max(), 3)
    result = {
        "date": date,
        "stock_code": stock_code,
        "bullish_days": fut_price_df[key].ge(price).sum(),
        "bullish_trend": is_bullish_or_bearish_trend(fut_price_df.to_dict(orient="records"), key=key),
        "highest_price": max_fut_price,
        "highest_percent": round(max_fut_price / price - 1, 3),
    }

    return result


def evaluate_bullish_trend(price_df, date_or_index, fut_size, key, a_share):
    pass
