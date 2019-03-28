import pandas as pd
from iexfinance.stocks import get_historical_data
from app.models import StockDailyPrice
from dateutil.relativedelta import relativedelta
from app import snp_500_df
from app.api.stock_prices.daily_price_dto import DailyPriceDto
from app.models import StockDailyPrice

def get_data(stock_ticker, start_date, end_date):
    get_all_snp500_data(start_date, end_date)
    if snp_500_df['Symbol'].eq(stock_ticker).any():
        data = StockDailyPrice.objects(stock_ticker=stock_ticker, date__lte=end_date, date__gte=start_date)
        data = [DailyPriceDto(stock_ticker, quote.date, quote.price).to_dict() for quote in data]
        return data
    else:
        data = fetch_missing_data(stock_ticker, start_date, end_date)
        return data

def get_all_snp500_data(start_date, end_date):
    data = StockDailyPrice.objects(date__lte=end_date, date__gte=start_date)
    data_df = pd.DataFrame()
    data_df['date'] = pd.date_range(start_date, end_date)
    data_df = data_df.set_index(['date'])
    for stock_ticker in snp_500_df['Symbol']:
        data_df[stock_ticker] = float('nan')
    for quote in data:
        data_df.at[quote.date, quote.stock_ticker] = quote.price
    data_df.dropna(how='all', inplace=True)
    return data_df

def fetch_missing_data(stock_ticker, start_date, end_date):
    if isinstance(stock_ticker, str):
        stock_data = get_historical_data(stock_ticker, start_date, end_date)
        stock_data = [DailyPriceDto(stock_ticker, value['open'], key).to_dict() for key, value in stock_data.items()]
        return stock_data
    elif isinstance(stock_ticker, list):
        stock_data = get_historical_data(stock_ticker, start_date, end_date)
        missing_data = []
        for key, value in stock_data.items():
            for key2, value2 in value.items():
                missing_data.append(DailyPriceDto(key, value2['open'], key2).to_dict())
        return missing_data

