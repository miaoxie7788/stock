"""
    Download data from yahoo finance.
"""

import os
from datetime import datetime, timedelta

from yahoo_fin.stock_info import get_data, get_dividends, get_splits


def get_stock_historical_data(stock_code, stock_path="data/asx_stock/csv"):
    """
        Get historical price, dividend and splits data for a stock.
    """
    # Create a folder for the stock.
    path = os.path.join(stock_path, stock_code)
    if not os.path.exists(path):
        os.mkdir(path)

    csv_filenames = os.listdir(path)
    for data_type in ["price", "dividend", "splits"]:
        # Get latest end_date. filename pattern: hist_price_{start date}_{end date}
        if csv_filenames:
            latest_end_date = max([str(csv_filename).split('.')[0].split('_')[-1] for csv_filename in csv_filenames
                                   if data_type in csv_filename])
        else:
            latest_end_date = None

        # Get hist data between latest_end_date and today.
        if latest_end_date:
            start_date = datetime.strptime(latest_end_date, "%Y%m%d") + timedelta(days=1)
        else:
            start_date = None

        end_date = datetime.today()
        if start_date and start_date >= end_date:
            raise Exception("The historical price data until {end_date} has been downloaded.".format(end_date=end_date))

        df = None
        if data_type == "price":
            if start_date:
                df = get_data(stock_code, start_date=start_date, end_date=end_date, index_as_date=False)
            else:
                df = get_data(stock_code, end_date=end_date, index_as_date=False)
                start_date = df["date"].min()
        elif data_type == "dividend":
            try:
                get_dividends(stock_code)
            except KeyError:
                print("{stock_code} does not have historical dividend data.".format(stock_code=stock_code))
            except AssertionError:
                print("{stock_code} does not have historical dividend data.".format(stock_code=stock_code))
            else:
                if start_date:
                    df = get_dividends(stock_code, start_date=start_date, end_date=end_date, index_as_date=False)
                else:
                    df = get_dividends(stock_code, end_date=end_date, index_as_date=False)
                    start_date = df["date"].min()
        elif data_type == "splits":
            try:
                get_splits(stock_code)
            except KeyError:
                print("{stock_code} does not have historical splits data.".format(stock_code=stock_code))
            except AssertionError:
                print("{stock_code} does not have historical splits data.".format(stock_code=stock_code))
            else:
                if start_date:
                    df = get_splits(stock_code, start_date=start_date, end_date=end_date, index_as_date=False)
                else:
                    df = get_splits(stock_code, end_date=end_date, index_as_date=False)
                    start_date = df["date"].min()
        else:
            raise Exception("Unknown data type.")

        # Export the csv to data/asx_stock/{asx_code}
        if df is not None:
            csv_filename = "hist_" + data_type + "_" + start_date.strftime("%Y%m%d") + "_" + end_date.strftime(
                "%Y%m%d") + ".csv"
            print(csv_filename)
            df.to_csv(os.path.join(path, csv_filename), header=True, index=False)


def get_asx_stock_historical_data(asx_stock_codes):
    for asx_stock_code in asx_stock_codes:
        print("\nStart downloading historical data for {stock_code}".format(stock_code=asx_stock_code))
        get_stock_historical_data(asx_stock_code)
        print("The historical data for {stock_code} has been downloaded. \n".format(stock_code=asx_stock_code))


if __name__ == "__main__":
    # Get asx stock historical price data.
    asx_stock_watchlist = ["tls.ax", "wbc.ax", "nov.ax", "cba.ax", "hack.ax", "ltr.ax"]
    get_asx_stock_historical_data(asx_stock_watchlist)
