from app import app
from app.models import StockDailyPrice
from app.api.stock_fetcher.get_data import fetch_missing_data
from datetime import datetime
from dateutil.relativedelta import relativedelta
import sys
from app.models import StockDailyPrice

# app.app_context().push()


def fetch_snp500_data(stock_tickers):
    try:
        # app.app_context().push()
        current_date = datetime.now()
        missing_data = fetch_missing_data(stock_tickers, current_date-relativedelta(years=5), current_date)
        for index, row in missing_data.iterrows():
            for ticker in stock_tickers:
                stockDailyPrice = StockDailyPrice(ticker=ticker, date=index, price=row[ticker])
                stockDailyPrice.save()
    except:
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())