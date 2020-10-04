"""
    Download data from yahoo finance.
"""

import os

from yahoo_fin.stock_info import get_data, get_dividends, get_splits


def get_stock_historical_data(stock_code, start_date=None, end_date=None, path="data/asx_stock/csv"):
    """
        Get historical price, dividend and splits data for a stock between start_date and end_date.
    """
    # Make a folder for the stock if it does not exist.
    stock_path = os.path.join(path, stock_code)
    if not os.path.exists(stock_path):
        os.mkdir(stock_path)

    # Get historical data.
    stock_info_func_dict = {
        "price": get_data,
        "dividend": get_dividends,
        "splits": get_splits
    }

    for data_type in stock_info_func_dict:
        try:
            df = stock_info_func_dict[data_type](ticker=stock_code,
                                                 start_date=start_date,
                                                 end_date=end_date,
                                                 index_as_date=False)

            # Get start_date and end_date.
            start_date = df["date"].min()
            end_date = df["date"].max()

            # Make the filename for the historical data.
            filename = os.path.join(stock_path, "hist_{date_type}_{start_date}_{end_date}.csv".
                                    format(date_type=data_type,
                                           start_date=start_date.strftime("%Y%m%d"),
                                           end_date=end_date.strftime("%Y%m%d")))

            if not os.path.exists(filename):
                df.to_csv(filename, header=True, index=False)
                print("Historical {data_type} data are downloaded for {stock_code} between {start_date} and {end_date}".
                      format(stock_code=stock_code, data_type=data_type, start_date=start_date, end_date=end_date))
        except KeyError:
            print("Historical {data_type} data are not available for {stock_code}.".
                  format(stock_code=stock_code, data_type=data_type))


if __name__ == "__main__":
    # Get asx stock historical data.
    # asx_stock_watchlist = ["tls.ax", "wbc.ax", "nov.ax", "cba.ax", "hack.ax", "ltr.ax"]

    # Get SZ stock historical data.

    sz_stocks = ["300655.SZ", "300122.SZ", "002007.SZ", "300185.SZ", "002594.SZ", "002625.SZ",
                 "000625.SZ", "300750.SZ", "000333.SZ", "002475.SZ", "000725.SZ", "300730.SZ", "002230.SZ",
                 "000002.SZ", "002285.SZ", "000656.SZ", "000011.SZ", "000069.SZ", "000006.SZ", "300369.SZ"]

    for stock in sz_stocks:
        get_stock_historical_data(stock, path="data/sz_stock/csv")
