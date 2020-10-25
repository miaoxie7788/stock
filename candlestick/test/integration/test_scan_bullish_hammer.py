import os

import pandas as pd

pd.set_option('display.max_columns', None)

# def test_stock(stock_code, stock_params, path="data/asx_stock/"):
#     # print("Testing {stock_code}".format(stock_code=stock_code))
#
#     code, market = stock_code.split(".")
#     filename_regex = "{market}_{code}_{date_type}_{start_date}_{end_date}.csv".format(
#         market=market,
#         code=code,
#         date_type="price",
#         start_date=r"\d{8}",
#         end_date=r"\d{8}")
#
#     filenames = os.listdir(path)
#     price_filename = os.path.join(path,
#                                   [filename for filename in filenames if re.match(filename_regex, filename)][0])
#
#     price_df = pd.read_csv(price_filename)
#
#     windows = evaluate_bullish_hammer(price_df, **stock_params)
#
#     windows_df = evaluate_any_higher_price(windows, key="high", a_share=True)
#     windows_df0 = windows_df.loc[windows_df["is_hammer_signal"]]
#
#     n = len(windows_df)
#     n0 = len(windows_df0)
#
#     rate = len(windows_df[windows_df["higher_fut_price"] >= 0]) / n
#     if n0 == 0:
#         rate0 = 0
#     else:
#         rate0 = len(windows_df0[windows_df0["higher_fut_price"] >= 0]) / n0
#
#     # scale: billion
#     trade_scale = round(price_df.apply(lambda row: row["volume"] * row["close"], axis="columns").mean() / 1000000000, 3)
#
#     result = {
#         "stock_code": stock_code,
#         "trade_scale": trade_scale,
#         "trade_days": n,
#         "n_hammer_signal": n0,
#         "benchmark_success_rate": round(rate, 3),
#         "success_rate": round(rate0, 3),
#         "improvement": round(rate0 / rate - 1, 3),
#         "method": "any_higher_high_price",
#         **stock_params
#     }
#
#     print(result)
#     print(windows_df0[["date", "higher_fut_price"]])
#     debug(windows_df0)
#
#     return result


if __name__ == "__main__":
    # asx_stocks = ["abp.ax", "apt.ax", "boq.ax", "bpt.ax", "ctx.ax", "car.ax", "csl.ax", "dhg.ax", "dmp.ax", "fph.ax",
    #               "gem.ax", "hvn.ax", "ire.ax", "jbh.ax", "mgr.ax", "mpl.ax", "tls.ax", "wbc.ax", "orh.ax", "cba.ax", ]
    #
    # params_dict = {
    #     "his_size": 5,
    #     "fut_size": 2,
    #     "abs_slope": 0.01,
    #     "t1": 1,
    #     "t3": 1.5,
    #     "small_body": 0.1,
    #     "enhanced": True
    # }
    #
    # # asx_stocks = ["apt.ax"]
    #
    # result_df = pd.DataFrame([test_stock(stock, params_dict, "data/asx_stock/csv") for stock in asx_stocks])
    # result_df.to_csv("asx_scan_hammer_results2.csv", index=False, header=True)

    with open("data/hs_stock_codes") as f:
        hs_stocks = [stock.strip() for stock in f.readlines()]

    hs_params = {
        "bullish_hammer_params": {
            "hammer_params": {"t1": 3,
                              "t3": 4,
                              "small_body": 0.05},
            "key": "low",
            "abs_slope": 0.25,
            "enhanced": True,
        },
        "ref_size": 5,
        "fut_size": 2,
    }
    # 600909.ss
    # 601878.ss
    # 688008.ss
    # 688018.ss
    # 300339.sz
    # 603368.ss     0.82        2%

    hs_stocks = ["000997.sz"]
    result_df = pd.DataFrame([test_stock(stock, hs_params, "data/stock") for stock in hs_stocks])
    # result_df.to_csv("hs_scan_hammer_results2.csv", index=False, header=True)
