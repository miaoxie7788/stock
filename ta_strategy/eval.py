import plotly.graph_objects as go

from ta_indicator.trend import is_upward_or_downward_trend


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
def eval_increase(y):
    """
        Evaluate increase for a couple of consecutive values (prices or volumes).

    """
    if any(y.isnull()):
        is_increase = False
        significance = 0
        max_increase = 0
    else:
        y = y.to_list()
        upward_or_downward, _ = is_upward_or_downward_trend(y)

        if upward_or_downward == "upward":
            is_increase = True
        else:
            is_increase = False

        significance = sum([v > y[0] for v in y[1:]]) / (len(y) - 1)
        max_increase = round((max(y[1:]) - y[0]) / y[0], 3)

    return is_increase, significance, max_increase
