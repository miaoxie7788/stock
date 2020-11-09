"""
    Scan candlestick patterns.
"""

import os
from datetime import datetime, timedelta

import pandas as pd

from candlestick.core.pattern import is_bullish_hammer
from stock_market_data.yahoo import get_stock_historical_data, export_stock_info_df_to_csv


def get_data(last_days=21, watchlist="data/candlestick/hs_watchlist", stock_path="data/candlestick/stock"):
    """
        Get historical data for stocks presented in the watchlist between today and today-last_days.
        Note, last_days should be larger than his_size.
    """

    # Read watchlist.
    with open(watchlist) as f:
        stock_codes = [line.strip() for line in f.readlines()]

    today = datetime.today()
    start_date = today - timedelta(days=last_days)
    end_date = today + timedelta(days=1)

    for stock_code in stock_codes:
        dfs = get_stock_historical_data(stock_code=stock_code,
                                        data_types=["price"],
                                        start_date=start_date,
                                        end_date=end_date,
                                        interval="1d")

        export_stock_info_df_to_csv(dfs, path=stock_path)


def scan_bullish_hammer(price_df, date_or_index, ref_size, hammer_params, market_top_or_bottom_params, enhanced):
    """
        Scan whether the trade day (given by date) is a bullish hammer, according to historical ref_size trade days.

            date  open  high   low  close  adjclose    volume     ticker
        0  2020-10-09  9.44  9.48  9.40   9.42      9.42  39772687  600000.SS
        1  2020-10-12  9.45  9.63  9.42   9.59      9.59  66671637  600000.SS
        2  2020-10-13  9.58  9.58  9.52   9.54      9.54  28059097  600000.SS
        3  2020-10-14  9.54  9.56  9.50   9.53      9.53  42969217  600000.SS
        4  2020-10-15  9.54  9.72  9.53   9.62      9.62  66146732  600000.SS
        5  2020-10-16  9.61  9.77  9.60   9.72      9.72  74850236  600000.SS
        6  2020-10-19  9.73  9.93  9.64   9.65      9.65  84532385  600000.SS
        7  2020-10-20  9.63  9.65  9.51   9.58      9.58  46687029  600000.SS
        8  2020-10-21  9.58  9.70  9.51   9.70      9.70  61622129  600000.SS

    """
    # Ensure the price_df is sorted in ascending order according to date.
    price_df = price_df.sort_values(by="date", axis='index', ascending=True) \
        .reset_index().drop(labels="index", axis="columns")

    # By default, it scans the last candlestick in the price_df.
    index = len(price_df) - 1
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

    if index < ref_size:
        print("{stock_code} does not have {ref_size} ref candlesticks."
              .format(ref_size=ref_size, stock_code=stock_code))
        return None

    candlestick = price_df.iloc[index].to_dict()
    ref_candlesticks = price_df.iloc[index - ref_size:index].to_dict(orient="records")

    if is_bullish_hammer(candlestick, ref_candlesticks, hammer_params, market_top_or_bottom_params, enhanced):
        print("A bullish hammer is found for {stock} on {day}".format(stock=stock_code, day=date))
        pattern = {"date": date, "stock_code": stock_code, "pattern": "bullish_hammer"}
        return pattern

    return None


def scan_patterns(params, watchlist="data/candlestick/hs_watchlist", stock_path="data/candlestick/stock"):
    with open(watchlist) as f:
        stock_codes = [line.strip() for line in f.readlines()]

    patterns = list()
    for stock_code in stock_codes:
        code, market = stock_code.split(".")
        # short_csv_filename.
        name = "{market}_{code}_{date_type}.csv".format(
            market=market,
            code=code,
            date_type="price")

        filename = os.path.join(stock_path, name)
        if os.path.exists(filename):
            price_df = pd.read_csv(filename)
        else:
            print("{stock} does not have data.".format(stock=stock_code))
            continue

        date_or_index = params["date_or_index"]
        ref_size = params["ref_size"]
        hammer_param = params["hammer_params"]
        market_top_or_bottom_params = params["market_top_or_bottom_params"]
        enhanced = params["enhanced"]

        pattern = scan_bullish_hammer(price_df, date_or_index, ref_size, hammer_param, market_top_or_bottom_params,
                                      enhanced)
        if pattern:
            patterns.append(pattern)

    return patterns


if __name__ == "__main__":
    # get_data(watchlist="data/candlestick/hs_watchlist", last_days=14, stock_path="data/candlestick/stock")
    get_data(watchlist="data/candlestick/asx_watchlist", last_days=14, stock_path="data/candlestick/stock")

    # hs_params = {
    #     "hammer_params": {"t1": 1,
    #                       "t3": 2,
    #                       "small_body": 0.1},
    #     "market_top_or_bottom_params": {"key": "low",
    #                                     "abs_slope": 0.05},
    #
    #     "enhanced": True,
    #
    #     "ref_size": 5,
    #     "date_or_index": None
    # }
    #
    # hs_patterns = scan_patterns(params=hs_params,
    #                             watchlist="data/candlestick/hs_watchlist",
    #                             stock_path="data/candlestick/stock")
    #
    # pd.DataFrame(hs_patterns).to_csv("data/candlestick/results/hs_stock_patterns_{today}.csv".format(
    #     today=datetime.today().strftime("%Y%m%d")),
    #     index=False,
    #     header=True)

    asx_params = {
        "hammer_params": {"t1": 1,
                          "t3": 2,
                          "small_body": 0.1},
        "market_top_or_bottom_params": {"key": "low",
                                        "abs_slope": 0.02},

        "enhanced": True,

        "ref_size": 5,
        "date_or_index": None
    }

    asx_patterns = scan_patterns(params=asx_params,
                                 watchlist="data/candlestick/asx_watchlist",
                                 stock_path="data/candlestick/stock")

    pd.DataFrame(asx_patterns).to_csv("data/candlestick/results/asx_stock_patterns_{today}.csv".format(
        today=datetime.today().strftime("%Y%m%d")),
        index=False,
        header=True)
