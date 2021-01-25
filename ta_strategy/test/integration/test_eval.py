import pandas as pd

from ta_stock_market_data.yahoo import stock_data_dfs_read_csv
from ta_strategy.eval import eval_increase
from ta_strategy.s01 import exec_s01

if __name__ == '__main__':
    watchlist = "data/test/asx_watchlist"
    # stock_market_data_path = get_stock_market_data(watchlist=watchlist,
    #                                                data_types=["price"],
    #                                                path="data/test")

    stock_market_data_path = "data/test/asx_earliest_20210112_1d"
    with open(watchlist) as f:
        stock_codes = [line.strip() for line in f.readlines()]

    results = list()
    for stock_code in stock_codes[4:5]:
        print(stock_code)
        dfs = stock_data_dfs_read_csv(stock_code, stock_market_data_path)

        if "price" not in dfs:
            print("{stock} does not have price data.".format(stock=stock_code))
            continue
        else:
            df = dfs["price"]

        n = len(df)
        window_size = 10
        results = list()

        t = 0
        while t < n:
            exec_date = df.iloc[t]["date"]
            if exec_s01(df, exec_date):
                # print(exec_date, stock_code)
                if t + window_size < n:
                    y = df.iloc[t:t + window_size + 1]["close"]

                    is_increase, significance, max_increase = eval_increase(y)

                    result = {"stock": stock_code, "date": exec_date, "increased": is_increase,
                              "max_increase": max_increase, "significance": significance}
                    print(result)
                    results.append(result)
                    t = t + window_size + 1
            else:
                t += 1

        results_df = pd.DataFrame(results)
        print(len(results_df.loc[results_df["increased"]]) / len(results_df))
        print(len(results_df.loc[results_df["max_increase"] > 0]) / len(results_df))
        # results_df.to_csv("result.csv")
