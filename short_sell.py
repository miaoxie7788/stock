"""
    Download daily short sell data from https://www.asx.com.au/data/shortsell.txt.
"""

import re
from datetime import date, datetime

import pandas as pd
import requests


def get_asx_daily_short_sell(url="https://www.asx.com.au/data/shortsell.txt"):
    """
        Download daily ASX short sell data and save as data/short_sell/asx_short_sell_yyyymmdd.txt.
    """
    resp = requests.get(url, allow_redirects=True)

    today = date.today().strftime("%Y%m%d")
    txt_filename = 'data/short_sell/txt/asx_short_sell_{date}.txt'.format(date=today)

    with open(txt_filename, 'wb') as f:
        f.write(resp.content)

    return resp.status_code


def transform_asx_daily_short_sell(short_sell_date):
    """
            Transform the ASX short sell data of the given day from txt to csv.
    """
    txt_filename = 'data/short_sell/txt/asx_short_sell_{date}.txt'.format(date=short_sell_date)

    columns = ["asx_code", "company_name", "product_class", "reported_gross_short_sells", "issued_capital",
               "percentage"]

    with open(txt_filename, 'rb') as f:
        # Read first row and extract date.
        row = f.readline().decode("utf-8")
        # Re-format the date.
        today = datetime.strptime(re.search(r"\d{2}-\w{3}-\d{4}", row).group(), "%d-%b-%Y").strftime("%Y%m%d")

        # Skip next 7 rows.
        for _ in range(7):
            next(f)

        df = list()
        for row in f:
            row = row.decode("utf-8")
            # Each row is split at the beginning and the end of "product_class".
            left_row = row[:42]
            mid_row = row[42:53]
            right_row = row[53:]

            asx_code, company_name = left_row.split(" ", 1)
            company_name = company_name.strip()
            product_class = mid_row.strip()

            reported_gross_short_sells, issued_capital, percentage = right_row.split()
            reported_gross_short_sells = int(reported_gross_short_sells.replace(",", ""))
            issued_capital = int(issued_capital.replace(",", ""))
            percentage = float(percentage)

            values = [asx_code, company_name, product_class, reported_gross_short_sells, issued_capital, percentage]

            df.append(dict(zip(columns, values)))

        df = pd.DataFrame(df)

        csv_filename = 'data/short_sell/csv/asx_short_sell_{date}.csv'.format(date=today)
        df.to_csv(csv_filename, header=True, index=False)


if __name__ == "__main__":
    # execute only if run as a script
    # get_asx_daily_short_sell()

    days = ["20200911", "20200912", "20200913", "20200914", "20200915", "20200916"]

    for day in days:
        transform_asx_daily_short_sell(day)
