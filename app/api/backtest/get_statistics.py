import pandas as pd
import numpy as np
from copy import copy

from app.api.stock_fetcher.get_data import get_data
from app.api.backtest.data_manipulation import dict_to_dataframe


def prepare_dataframe(portfolio, start_date, end_date):

    # portfolio is a dict mapping stocks to weights
    # print(portfolio.keys())
    # print(portfolio)

    df = get_data(list(portfolio.keys()), start_date, end_date)
    df.dropna(inplace=True)

    return df


def compute_total_value(prices_df, initial_amount, portfolio):
    """Computes monetary value of portfolio from prices dataframe provided

    Arguments:
        prices_df {pandas dataframe} -- Dataframe containing prices of stocks with timestamps. Columns are stock tickers, rows are timestamps.
        initial_amount {int} -- Initial monetary value of portfolio
        portfolio {dict} -- Dictionary containing stock tickers as keys, and percentage allocations as values

    Returns:
        Pandas Dataframe -- Dataframe containing total portfolio value/worth at different timestamps.
    """
    # Get portfolio data
    initial_portfolio_in_quantities = copy(portfolio)
    initial_prices = prices_df.iloc[0]  # Calculate initial prices of each stock

    # Calculate initial quantities of each stock owned, depending on percentage allocations from portfolio
    # Basically, quantity of stock A is (percentage allocation)*(initial amount) / stock price
    for key in portfolio.keys():
        initial_portfolio_in_quantities[key] = (initial_amount * portfolio[key]) / prices_df.iloc[0][key]

    # Create dataframe of daily returns
    prices_df = pd.concat([(prices_df[stock].diff() * initial_portfolio_in_quantities[stock])
                           for stock in list(portfolio.keys())], axis=1, keys=list(portfolio.keys())).sum(axis=1).dropna()

    # Add daily returns to get cumulative sum, then add initial portfolio value
    prices_df = prices_df.cumsum()
    prices_df = prices_df + initial_amount

    return prices_df


def compute_daily_returns(prices_over_time):

    df = prices_over_time
    df['daily_returns'] = df.pct_change()
    df.dropna(inplace=True)
    return df


def compute_moving_average(prices_over_time, window):

    df = prices_over_time

    df['ma'] = np.nan
    df['ma'] = df.rolling(window=window).mean()

    return df


def compute_moving_standard_deviation(prices_over_time, window):

    df = prices_over_time

    df['mstd'] = np.nan
    df['mstd'] = df.rolling(window=window).std()

    return df


def compute_statistics(prices_df, initial_amount, portfolio, window):

    df = prices_df

    df = compute_total_value(df, initial_amount, portfolio)

    df = df.to_frame("total")  # need to turn pandas series to dataframe to add columns

    df = compute_moving_average(df, window)
    df = compute_moving_standard_deviation(df, window)

    df['upper'] = df['ma'] + (df['mstd'] * 2)
    df['lower'] = df['ma'] - (df['mstd'] * 2)

    # df.dropna(inplace=True)
    df = df.bfill();    

    return df
