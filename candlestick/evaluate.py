import numpy as np
import plotly.graph_objects as go


def plot_candlestick(price_df):
    fig = go.Figure(data=[go.Candlestick(
        x=price_df['date'],
        open=price_df['open'],
        high=price_df['high'],
        low=price_df['low'],
        close=price_df['close'])])

    fig.show()


def evaluate(eval_dict, key="close", print_detail=True):
    """"
        Each item in eval_dict is ('date', neighbouring_candlesticks).

        E.g., windows_size = 3,
        c-3, c-2, c-1, c0, c1, c2

        It evaluates if there is any price of [c1, c2] (by default close price) higher than price of c0. If yes,
        it indicates "success"; otherwise "failure".
    """
    success = 0
    for date, candlesticks in eval_dict.items():

        # Convert df to list of candlesticks.
        candlesticks = candlesticks.to_dict(orient="records")
        # Compute window_size.
        window_size = int(len(candlesticks) / 2)

        if candlesticks:
            present_candlestick = candlesticks[window_size]
            future_candlesticks = candlesticks[window_size + 1:]

            present_price = present_candlestick[key]
            future_prices = [candlestick[key] for candlestick in future_candlesticks if not np.isnan(candlestick[key])]

            if any(future_price > present_price for future_price in future_prices):
                success += 1
                if print_detail:
                    print("It succeeds on {date}".format(date=date))
            else:
                if print_detail:
                    print("It fails on {date}".format(date=date))

    if len(eval_dict) != 0:
        success_rate = success / len(eval_dict)
        if print_detail:
            print("The successful rate is: {rate}".format(rate=success_rate))
    else:
        success_rate = 0

    return success_rate
