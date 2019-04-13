import pandas as pd

from flask import jsonify

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

from app.api.stock_fetcher.get_data import get_data, get_all_snp500_data
from app.api.backtest import backtest_portfolio

from datetime import datetime


def max_sharpe(parameters):

    print("From optimizer: ", parameters)

    stocks_df = get_data(parameters["ticker_list"], datetime.strptime(parameters["start_date"], '%Y-%m-%d'),
       datetime.strptime(parameters["end_date"], '%Y-%m-%d'))

    print(stocks_df.head())

    mu = expected_returns.mean_historical_return(stocks_df)

    S = risk_models.sample_cov(stocks_df)

    ef = EfficientFrontier(mu, S, weight_bounds=(0, 1))

    raw_weights = ef.max_sharpe()

    cleaned_weights = ef.clean_weights()

    # cleaned_weights = {k: round(v * 100, 3) for k, v in cleaned_weights.items() if v != 0}
    cleaned_weights = {k: v for k, v in cleaned_weights.items() if v != 0}

    print(cleaned_weights)

    # backtest_results = get_daily_returns(cleaned_weights, parameters["start_date"], parameters["end_date"])

    backtest_results = backtest_portfolio(prices_df=stocks_df, portfolio=cleaned_weights, initial_amount=int(parameters[
      "initial_amount"]), start_date=parameters["start_date"], end_date=parameters["end_date"])

    print(backtest_results.describe())

    backtest_results_dict = backtest_results.to_dict()

    output = {

    "weights": {
    "labels": list(cleaned_weights.keys()),
            # Convert into percentages instead of proportions
            "data":  [round(x * 100, 2) for x in list(cleaned_weights.values())]
            },

            "performance": {
            "labels": list(backtest_results_dict.keys()),
            "data": list(backtest_results_dict.values())
            }
            }

    return output

def min_volatility(parameters):

    print("From optimizer: ", parameters)

    stocks_df = get_data(parameters["ticker_list"], datetime.strptime(parameters["start_date"], '%Y-%m-%d'),
       datetime.strptime(parameters["end_date"], '%Y-%m-%d'))

    print(stocks_df.head())

    mu = expected_returns.mean_historical_return(stocks_df)

    S = risk_models.sample_cov(stocks_df)

    ef = EfficientFrontier(mu, S, weight_bounds=(0, 1))

    raw_weights = ef.max_sharpe()

    cleaned_weights = ef.clean_weights()

# cleaned_weights = {k: round(v * 100, 3) for k, v in cleaned_weights.items() if v != 0}
    cleaned_weights = {k: v for k, v in cleaned_weights.items() if v != 0}

    print(cleaned_weights)

    # backtest_results = get_daily_returns(cleaned_weights, parameters["start_date"], parameters["end_date"])

    backtest_results = backtest_portfolio(prices_df=stocks_df, portfolio=cleaned_weights, initial_amount=int(parameters[
      "initial_amount"]), start_date=parameters["start_date"], end_date=parameters["end_date"])

    print(backtest_results.describe())

    backtest_results_dict = backtest_results.to_dict()

    output = {

    "weights": {
    "labels": list(cleaned_weights.keys()),
            # Convert into percentages instead of proportions
            "data":  [round(x * 100, 2) for x in list(cleaned_weights.values())]
            },

            "performance": {
            "labels": list(backtest_results_dict.keys()),
            "data": list(backtest_results_dict.values())
            }
            }

    return output

def min_volatility_target(parameters):

    print("From optimizer: ", parameters)

    stocks_df = get_data(parameters["ticker_list"], datetime.strptime(parameters["start_date"], '%Y-%m-%d'),
       datetime.strptime(parameters["end_date"], '%Y-%m-%d'))

    print(stocks_df.head())

    mu = expected_returns.mean_historical_return(stocks_df)

    S = risk_models.sample_cov(stocks_df)

    ef = EfficientFrontier(mu, S, weight_bounds=(0, 1))

    raw_weights = ef.max_sharpe()

    cleaned_weights = ef.clean_weights()

    # cleaned_weights = {k: round(v * 100, 3) for k, v in cleaned_weights.items() if v != 0}
    cleaned_weights = {k: v for k, v in cleaned_weights.items() if v != 0}

    print(cleaned_weights)

    # backtest_results = get_daily_returns(cleaned_weights, parameters["start_date"], parameters["end_date"])

    backtest_results = backtest_portfolio(prices_df=stocks_df, portfolio=cleaned_weights, initial_amount=int(parameters[
      "initial_amount"]), start_date=parameters["start_date"], end_date=parameters["end_date"])

    print(backtest_results.describe())

    backtest_results_dict = backtest_results.to_dict()

    output = {

    "weights": {
    "labels": list(cleaned_weights.keys()),
            # Convert into percentages instead of proportions
            "data":  [round(x * 100, 2) for x in list(cleaned_weights.values())]
            },

            "performance": {
            "labels": list(backtest_results_dict.keys()),
            "data": list(backtest_results_dict.values())
            }
            }

    return output

def max_return_target(parameters):

    print("From optimizer: ", parameters)

    stocks_df = get_data(parameters["ticker_list"], datetime.strptime(parameters["start_date"], '%Y-%m-%d'),
       datetime.strptime(parameters["end_date"], '%Y-%m-%d'))

    print(stocks_df.head())

    mu = expected_returns.mean_historical_return(stocks_df)

    S = risk_models.sample_cov(stocks_df)

    ef = EfficientFrontier(mu, S, weight_bounds=(0, 1))

    raw_weights = ef.max_sharpe()

    cleaned_weights = ef.clean_weights()

    # cleaned_weights = {k: round(v * 100, 3) for k, v in cleaned_weights.items() if v != 0}
    cleaned_weights = {k: v for k, v in cleaned_weights.items() if v != 0}

    print(cleaned_weights)

    # backtest_results = get_daily_returns(cleaned_weights, parameters["start_date"], parameters["end_date"])

    backtest_results = backtest_portfolio(prices_df=stocks_df, portfolio=cleaned_weights, initial_amount=int(parameters[
      "initial_amount"]), start_date=parameters["start_date"], end_date=parameters["end_date"])

    print(backtest_results.describe())

    backtest_results_dict = backtest_results.to_dict()

    output = {

    "weights": {
    "labels": list(cleaned_weights.keys()),
            # Convert into percentages instead of proportions
            "data":  [round(x * 100, 2) for x in list(cleaned_weights.values())]
            },

            "performance": {
            "labels": list(backtest_results_dict.keys()),
            "data": list(backtest_results_dict.values())
            }
            }

    return output

def target_return_volatility(parameters):
    
    """Basic optimization function for the basic interface.

    Function tries to match a portfolio volatility and return.
    
    Arguments:
        parameters {dict} -- 
    
    Returns:
        [type] -- [description]
    """

    print("From optimizer: ", parameters)

    stocks_df = get_all_snp500_data(datetime.strptime(parameters["start_date"], '%Y-%m-%d'),
       datetime.strptime(parameters["end_date"], '%Y-%m-%d'))
    print("Stocks df")
    print(stocks_df.head())

    mu = expected_returns.mean_historical_return(stocks_df)

    S = risk_models.sample_cov(stocks_df)

    ef = EfficientFrontier(mu, S, weight_bounds=(0, 1))


    raw_weights = ef.max_sharpe()

    cleaned_weights = ef.clean_weights()

    # cleaned_weights = {k: round(v * 100, 3) for k, v in cleaned_weights.items() if v != 0}
    cleaned_weights = {k: v for k, v in cleaned_weights.items() if v != 0}

    print(cleaned_weights)

    # backtest_results = get_daily_returns(cleaned_weights, parameters["start_date"], parameters["end_date"])

    backtest_results = backtest_portfolio(prices_df=stocks_df, portfolio=cleaned_weights, initial_amount=1000, start_date=parameters["start_date"], end_date=parameters["end_date"])

    print(backtest_results.describe())

    backtest_results_dict = backtest_results.to_dict()

    output = {

    "weights": {
    "labels": list(cleaned_weights.keys()),
            # Convert into percentages instead of proportions
            "data":  [round(x * 100, 2) for x in list(cleaned_weights.values())]
            },

            "performance": {
            "labels": list(backtest_results_dict.keys()),
            "data": list(backtest_results_dict.values())
            }
            }

    return output



