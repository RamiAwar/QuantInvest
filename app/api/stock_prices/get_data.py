import pandas as pd
from iexfinance.stocks import get_historical_data
from app.models import StockDailyPrice
from dateutil.relativedelta import relativedelta
from app import snp_500_df
from app.api.stock_prices.daily_price_dto import DailyPriceDto
from app.models import StockDailyPrice

def get_data(stock_ticker, start_date, end_date):
    if snp_500_df['Symbol'].eq(stock_ticker).any():
        data = StockDailyPrice.objects(stock_ticker=stock_ticker, date__lte=end_date, date__gte=start_date)
        data = [DailyPriceDto(stock_ticker, quote.date, quote.price).to_dict() for quote in data]
        return data
    else:
        data = fetch_missing_data(stock_ticker, start_date, end_date)
        return data

def fetch_missing_data(stock_ticker, start_date, end_date):
    stock_data = get_historical_data(stock_ticker, start_date, end_date)
    stock_data = [DailyPriceDto(stock_ticker, value['open'], key).to_dict() for key, value in stock_data.items()]
    return stock_data

