import re

with open("data/hs_1601_", "r", encoding="utf8") as f1:
    lines = f1.readlines()

with open("data/hs_stock_codes_1601_", "w") as f2:
    for line in lines:
        stock_code = re.search(r"\w{2}\d{6}", line).group()

        mkt = stock_code[:2]
        code = stock_code[2:]

        if mkt == "sh":
            mkt = "ss"

        yahoo_stock_code = "{code}.{mkt}".format(code=code, mkt=mkt)
        f2.write(yahoo_stock_code)
        f2.write("\n")
