from datetime import datetime, timedelta
import pandas as pd
from iexfinance.stocks import get_historical_data
from app.models import StockDailyPrice
from dateutil.relativedelta import relativedelta
from app.stock_prices import snp_500_df
from app.stock_prices.daily_price_dto import DailyPriceDto

def get_data(stock_ticker, start_date, end_date):
    """ If stock is inside snp500, fetch from database, otherwise fetch from iexfinance api.
    """

    if snp_500_df['Symbol'].eq(stock_ticker).any():
        print('yup')
    else:
        data = fetch_missing_data(stock_ticker, start_date, end_date)
        return data

def fetch_missing_data(stock_ticker, start_date, end_date):
    stock_data = get_historical_data(stock_ticker, start_date, end_date)
    stock_data = [DailyPriceDto(stock_ticker, value['open'], key).to_dict() for key, value in stock_data.items()]
    return stock_data