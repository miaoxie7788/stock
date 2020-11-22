import re

import pandas as pd


def extract_hs_stock_codes():
    with open("../data/stock_codes/hs_listed_companies", "r", encoding="utf8") as f1:
        lines = f1.readlines()

    with open("../data/stock_codes/stock_code_list_hs", "w") as f2:
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
    df = pd.read_csv("../data/stock_codes/asx_listed_companies.csv")
    df["ASX code"].apply(lambda x: x.lower() + ".ax").to_csv("data/stock_code_list_asx", header=False, index=False)


def extract_asx_200_stock_codes():
    df = pd.read_csv("../data/stock_codes/asx_200_listed_companies.csv", skiprows=[0])
    df["Code"].apply(lambda x: x.lower() + ".ax").to_csv("data/stock_code_list_asx_200", header=False, index=False)


if __name__ == "__main__":
    # extract_hs_stock_codes()
    extract_asx_stock_codes()
    extract_asx_200_stock_codes()
