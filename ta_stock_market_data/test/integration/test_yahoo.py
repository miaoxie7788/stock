from datetime import date, timedelta

from ta_stock_market_data.yahoo import get_stock_market_data, get_stock_data, stock_data_dfs_to_csv, \
    stock_data_dfs_read_csv


def test_get_stock_historical_data():
    stock_code = "tls.ax"
    data_types = ["price", "dividend", "splits"]
    end_date = date.today()
    start_date = end_date - timedelta(days=7)

    dfs = get_stock_data(stock_code=stock_code,
                         data_types=data_types,
                         start_date=start_date,
                         end_date=end_date,
                         interval="1mo")

    stock_market_data_path = "data/test/"
    stock_data_dfs_to_csv(dfs, stock_market_data_path=stock_market_data_path)


def test_get_stock_market_data():
    watchlist = "data/test/asx_watchlist"
    data_types = ["price", "dividend", "splits"]
    end_date = date.today()
    start_date = end_date - timedelta(days=7)

    stock_market_data_path = get_stock_market_data(watchlist=watchlist,
                                                   relative_days=None,
                                                   data_types=data_types,
                                                   start_date=None,
                                                   end_date=None,
                                                   interval="1d",
                                                   path="data/test")

    print(stock_market_data_path)


def test_stock_data_dfs_read_csv():
    stock_code = "tls.ax"
    stock_market_data_path = "data/test/asx_earliest_20210110_1d"

    dfs = stock_data_dfs_read_csv(stock_code, stock_market_data_path)
    print(dfs)


if __name__ == "__main__":
    # test_get_stock_historical_data()
    # test_get_stock_market_data()
    test_stock_data_dfs_read_csv()
