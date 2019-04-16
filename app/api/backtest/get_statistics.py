import pandas as pd
from copy import copy

from app.api.stock_fetcher.get_data import get_data
from app.api.backtest.data_manipulation import dict_to_dataframe

def backtest_portfolio(portfolio, start_date, end_date, window=50):

    df = get_data(list(portfolio.keys()), start_date, end_date)
    df.dropna(inplace=True)
    df = compute_statistics(df, portfolio, window)

    return df

def compute_total_value(prices_over_time, portfolio):
    
    df = prices_over_time
    for column in df:
        df[column] = df[column].apply(lambda x: x * portfolio[column]) # multiply each column by the number of stocks bought to get total price

    stocks_list = list(df)
    df['total_value'] = df.sum(axis=1)
    df.drop(stocks_list, axis=1, inplace=True)
    
    return df

def compute_moving_average(prices_over_time, window):
    df = prices_over_time
    df['moving_average'] = float('nan')
    df['moving_average'] = df.rolling(window=window).mean()
    return df


def compute_moving_standard_deviation(prices_over_time, window):
    df = prices_over_time
    df['moving_standard_deviation'] = float('nan')
    df['moving_standard_deviation'] = df.rolling(window=window).std()
    return df


def compute_statistics(prices_over_time, portfolio, window):
    df = prices_over_time
    df = compute_total_value(df, portfolio)
    df = compute_moving_average(df, window)
    df = compute_moving_standard_deviation(df, window)
    return df
