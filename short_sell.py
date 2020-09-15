"""
    Download daily short sell data from https://www.asx.com.au/data/shortsell.txt.
"""

import io
import re
from datetime import date, datetime

import pandas as pd
import requests


def download_asx_daily_short_sell(url="https://www.asx.com.au/data/shortsell.txt"):
    """
        Download daily ASX short sell data and save as data/short_sell/asx_short_sell_yyyymmdd.txt.
    """
    resp = requests.get(url, allow_redirects=True)

    today = date.today().strftime("%Y%m%d")
    txt_filename = 'data/short_sell/asx_short_sell_{date}.txt'.format(date=today)

    with open(txt_filename, 'wb') as f:
        f.write(resp.content)

    return resp.status_code


def transform_asx_daily_short_sell(short_sell_date):
    """
        Transform the ASX short sell data of the given day from txt to csv.
    """

    txt_filename = 'data/short_sell/asx_short_sell_{date}.txt'.format(date=short_sell_date)

    with open(txt_filename, 'rb') as f:
        title = f.readline().decode("utf-8")
        real_date = re.search(r"\d{2}-\w{3}-\d{4}", title).group()
        real_date = datetime.strptime(real_date, "%d-%b-%Y").strftime("%Y%m%d")

        csv_filename = 'data/short_sell/asx_short_sell_{date}.csv'.format(date=real_date)

        columns = ["asx_code", "company_name", "product_class", "reported_gross_short_sells", "issued_capital",
                   "per"]
        buffer = io.StringIO(f.read().decode("utf-8"))
        print(buffer)
        df = pd.read_csv(filepath_or_buffer=buffer,
                         names=columns,
                         header=None,
                         delimiter=r"\s{4,}",
                         skiprows=[0, 1, 2, 3, 4, 5, 6],
                         )

        df.to_csv(csv_filename, header=True, index=False)

    # columns = ["asx_code", "company_name", "product_class", "reported_gross_short_sells", "issued_capital",
    #            "percentage_of_issued_capital_reported_as_short_sold"]

    # df = pd.read_csv(filepath_or_buffer=buffer,
    #                  names=columns,
    #                  header=None,
    #                  delimiter=r"\s{4,}",
    #                  skiprows=[0, 1, 2, 3, 4, 5, 6, 7],
    #                  )

    # print(df)


if __name__ == "__main__":
    # execute only if run as a script
    download_asx_daily_short_sell()
    # transform_asx_daily_short_sell("20200911")
