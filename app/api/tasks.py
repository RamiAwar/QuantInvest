from app import app
from app.models import StockDailyPrice
from app.api.stock_fetcher.get_data import fetch_missing_data
from datetime import datetime
from dateutil.relativedelta import relativedelta
import sys
from app.models import StockDailyPrice

def fetch_snp500_data(stock_tickers):
    try:
        latest_available_data = StockDailyPrice.objects.order_by('-date').first()
        latest_available_date = latest_available_data.date

        current_date = datetime.now()
        print("Fetching data in the range " + str(latest_available_date) + " " + str(current_date))
        missing_data = fetch_missing_data(stock_tickers, latest_available_date, current_date)

        for index, row in missing_data.iterrows():
            for ticker in stock_tickers:
                stockDailyPrice = StockDailyPrice(ticker=ticker, date=index, price=row[ticker])
                stockDailyPrice.save()
    except:
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())