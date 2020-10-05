from datetime import datetime, timedelta

from stock_market_data.yahoo import get_stock_historical_data

if __name__ == "__main__":
    path = "data/asx_stock/csv"
    stock_code = "car.ax"

    today = datetime.today()
    start_date = today - timedelta(days=1)

    get_stock_historical_data(stock_code, path=path)
