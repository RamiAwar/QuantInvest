from app import app
from app.models import StockDailyPrice
from app.api.stock_fetcher.get_data import fetch_missing_data
import sys
from app.models import StockDailyPrice


def fetch_snp500_data(stock_tickers, start_date, end_date):

    try:
        print("Fetching data in the range " + str(start_date) + " " + str(end_date))

        missing_data = fetch_missing_data(stock_tickers, start_date, end_date)

        for index, row in missing_data.iterrows():
            for ticker in stock_tickers:
                stockDailyPrice = StockDailyPrice(ticker=ticker, date=index, price=row[ticker])
                stockDailyPrice.save()

    except:
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())
