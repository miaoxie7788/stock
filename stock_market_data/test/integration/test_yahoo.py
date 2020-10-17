from datetime import datetime, timedelta

from stock_market_data.yahoo import get_stock_historical_data, export_stock_info_df_to_csv

if __name__ == "__main__":
    stock_code = "tls.ax"
    data_types = ["price", "dividend", "splits"]
    end_date = datetime.today()
    start_date = end_date - timedelta(days=7)

    dfs = get_stock_historical_data(stock_code=stock_code,
                                    data_types=data_types,
                                    start_date=None,
                                    end_date=end_date,
                                    full_csv_filename=True)

    path = "data/test/"
    export_stock_info_df_to_csv(dfs, path=path)
