from datetime import date, timedelta

from ta_stock_market_data.yahoo import get_stock_market_data, get_stock_data, export_stock_info_df_to_csv


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

    path = "data/test/"
    export_stock_info_df_to_csv(dfs, path=path)


def test_get_stock_market_data():
    watchlist = "data/test/asx_watchlist"
    data_types = ["price", "dividend"]
    end_date = date.today()
    start_date = end_date - timedelta(days=7)

    get_stock_market_data(watchlist=watchlist,
                          relative_days=100,
                          data_types=data_types,
                          start_date=None,
                          end_date=None,
                          interval="1d",
                          path="data/test")


if __name__ == "__main__":
    # test_get_stock_historical_data()
    test_get_stock_market_data()
