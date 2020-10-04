from datetime import datetime, timedelta

from stock_market_data.yahoo import get_stock_historical_data

if __name__ == "__main__":
    path = "data/sz_stock/csv"

    today = datetime.today()
    stock_code = "300369.SZ"
    start_date = today - timedelta(days=1)

    get_stock_historical_data(stock_code, None, None, path=path)
