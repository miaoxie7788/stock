import re

with open("hs_1_800", "r", encoding="utf8") as f1:
    lines = f1.readlines()

with open("hs_stock_codes", "w+") as f2:
    for line in lines:
        stock_code = re.search(r"\w{2}\d{6}", line).group()

        mkt = stock_code[:2]
        code = stock_code[2:]

        yahoo_stock_code = "{code}.{mkt}".format(code=code, mkt=mkt)
        f2.write(yahoo_stock_code)
        f2.write("\n")
