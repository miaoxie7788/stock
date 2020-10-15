"""
    Download data from yahoo finance.
"""

import os

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


def get_stock_historical_data(stock_code, data_types, start_date=None, end_date=None):
    """
        Get historical price, dividend and splits data for a stock between start_date and end_date.

    :param stock_code:      stock code, e.g., car.ax
    :param data_types:      ["price", "dividend", "splits"]
    :param start_date:      start date
    :param end_date:        end date
    :return:                stock_info_df_dict
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
            df = stock_info_func(ticker=stock_code,
                                 start_date=start_date,
                                 end_date=end_date,
                                 index_as_date=False)

            # Get start_date and end_date.
            start_date = df["date"].min()
            end_date = df["date"].max()

            # Split a stock_code into code and market, e.g, car.ax -> car, ax.
            code, market = stock_code.split(".")
            name = "{market}_{code}_{date_type}_{start_date}_{end_date}.csv".format(
                market=market,
                code=code,
                date_type=data_type,
                start_date=start_date.strftime("%Y%m%d"),
                end_date=end_date.strftime("%Y%m%d"))
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


if __name__ == "__main__":

    # Get HS stock historical data.
    with open("data/hs_stock_codes") as f:
        hs_stock_codes = [stock.strip() for stock in f.readlines()]

    hs_path = "data/stock"
    for hs_stock_code in hs_stock_codes:
        dfs = get_stock_historical_data(stock_code=hs_stock_code, data_types=["price"])
        export_stock_info_df_to_csv(dfs, hs_path)

    # Get ASX stock historical data.
    with open("data/asx_200_stock_codes") as f:
        asx_stock_codes = [stock.strip() for stock in f.readlines()]

    asx_path = "data/stock"
    for asx_stock_code in asx_stock_codes:
        dfs = get_stock_historical_data(stock_code=asx_stock_code, data_types=["price"])
        export_stock_info_df_to_csv(dfs, asx_path)
