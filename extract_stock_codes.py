import re

import pandas as pd


def extract_hs_stock_codes():
    with open("data/hs_listed_companies", "r", encoding="utf8") as f1:
        lines = f1.readlines()

    with open("data/hs_stock_codes", "w") as f2:
        for line in lines:
            stock_code = re.search(r"\w{2}\d{6}", line).group()

            mkt = stock_code[:2]
            code = stock_code[2:]

            if mkt == "sh":
                mkt = "ss"

            yahoo_stock_code = "{code}.{mkt}".format(code=code, mkt=mkt)
            f2.write(yahoo_stock_code)
            f2.write("\n")


def extract_asx_stock_codes():
    df = pd.read_csv("data/asx_listed_companies.csv")
    df["ASX code"].to_csv("data/asx_watchlist", header=False, index=False)


if __name__ == "__main__":
    # extract_hs_stock_codes()
    extract_asx_stock_codes()
