"""
    Download data from yahoo finance.
"""

import os
from datetime import date

from dateutil.relativedelta import relativedelta
from yahoo_fin.stock_info import get_data, get_dividends, get_splits


def export_stock_info_df_to_csv(stock_info_df_dict, path="data"):
    """
        Export dfs presented in stock_info_df to csvs.
    """
    # Make a folder if path does not exist.
    if not os.path.exists(path):
        os.mkdir(path)

    for name, df in stock_info_df_dict.items():
        df.to_csv(os.path.join(path, name), index=False, header=True)


def get_stock_data(stock_code, data_types, start_date=None, end_date=None, interval="1d"):
    """
        Get historical price, dividend and splits data for a stock between start_date and end_date.

    :param stock_code:              stock code, e.g., car.ax, 603678.ss, 002315.sz
    :param data_types:              ["price", "dividend", "splits"]
    :param start_date:              start date, datetime
    :param end_date:                end date, datetime
    :param interval:                "1d", "1wk" or "1mo"
    :return:                        stock_info_df_dict: {csv_filename: df, ...},
                                    csv_filename: {market}_{code}_{data_type}.csv
    """

    # Get historical data.
    stock_info_func_dict = {
        "price": get_data,
        "dividend": get_dividends,
        "splits": get_splits
    }

    stock_info_df_dict = dict()
    for data_type in data_types:
        stock_info_func = stock_info_func_dict[data_type]
        try:
            if data_type == "price":
                df = stock_info_func(ticker=stock_code,
                                     start_date=start_date,
                                     end_date=end_date,
                                     index_as_date=False,
                                     interval=interval)
            else:
                df = stock_info_func(ticker=stock_code,
                                     start_date=start_date,
                                     end_date=end_date,
                                     index_as_date=False)

            # Get start_date and end_date.
            start_date = df["date"].min()
            end_date = df["date"].max()

            # Split a stock_code into code and market, e.g, car.ax -> car, ax.
            code, market = stock_code.split(".")
            name = "{market}_{code}_{date_type}.csv".format(
                market=market,
                code=code,
                date_type=data_type)

            stock_info_df_dict[name] = df

            print("Historical {data_type} data are downloaded for {stock_code} between {start_date} and {end_date}".
                  format(stock_code=stock_code, data_type=data_type, start_date=start_date, end_date=end_date))

        except KeyError:
            print("Historical {data_type} data are not available for {stock_code} between the given dates".
                  format(stock_code=stock_code, data_type=data_type))

        except AssertionError:
            print("Historical {data_type} data are not available for {stock_code}.".
                  format(stock_code=stock_code, data_type=data_type))

    return stock_info_df_dict


def get_stock_market_data(watchlist, relative_days=None,
                          data_types=None, start_date=None, end_date=None, interval="1d", path="data"):
    """
        Get historical price data for stocks presented in the watchlist.

        Case 1:  start_date and end_date are given.

        Case 2:  start_date is given but not end_date.
                The default end_date is today.

        Case 3:  end_date is given but not start_date.
                If relative_days is given, start_date = end_date - relative_days;
                otherwise start_date=earliest.

        Case 4:  start_date and end_date are not given.
                If relative_days is given, start_date = today - relative_days and end_date=today;
                otherwise start_date=earliest and end_date = today.

        The data are exported into {path}/{stock_market}_{start_date}_{end_date}_{interval}.
    """

    # stock market: 'asx' or 'hs'.
    if "asx" in watchlist:
        market = "asx"
    elif "hs" in watchlist:
        market = "hs"
    else:
        market = ""

    # start_date and end_date.
    today = date.today()
    if start_date and not end_date:
        end_date = today
    elif not start_date and end_date:
        if relative_days:
            start_date = end_date - relativedelta(days=relative_days)
    elif not start_date and not end_date:
        end_date = today
        if relative_days:
            start_date = end_date - relativedelta(days=relative_days)

    # watchlist.
    with open(watchlist) as f:
        stock_codes = [line.strip() for line in f.readlines()]

    for stock_code in stock_codes:
        day_dfs = get_stock_data(stock_code=stock_code,
                                 data_types=data_types,
                                 start_date=start_date,
                                 end_date=end_date,
                                 interval=interval)

        if not start_date:
            start_date_str = "earliest"
        else:
            start_date_str = str(start_date).replace("-", "")

        end_date_str = str(end_date).replace("-", "")
        stock_market_data_path = os.path.join(path, "{market}_{start_date}_{end_date}_{interval}".format(
            market=market,
            start_date=start_date_str,
            end_date=end_date_str,
            interval=interval))

        export_stock_info_df_to_csv(day_dfs, path=stock_market_data_path)
