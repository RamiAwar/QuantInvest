import pandas as pd

from flask import jsonify

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

from app.api.stock_fetcher.get_data import get_data, get_all_snp500_data
from app.api.backtest import backtest_portfolio

from datetime import datetime
from dateutil.relativedelta import relativedelta


def max_sharpe(parameters):

    print("Optimizer received: ", parameters)

    stocks_df = get_data(parameters["ticker_list"], datetime.strptime(parameters["start_date"], '%Y-%m-%d'),
                         datetime.strptime(parameters["end_date"], '%Y-%m-%d'))

    mu = expected_returns.mean_historical_return(stocks_df)
    S = risk_models.sample_cov(stocks_df)
    ef = EfficientFrontier(mu, S, weight_bounds=(0, 1))

    raw_weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()

    cleaned_weights = {k: v for k, v in cleaned_weights.items() if v != 0}

    # get tuple of 3 values: (return, vol, sharpe)
    performance = ef.portfolio_performance()

    backtest_results = backtest_portfolio(prices_df=stocks_df, portfolio=cleaned_weights,
                                          initial_amount=int(parameters["initial_amount"]), window=50)

    labels = (list(backtest_results["total"].index))

    total_values = (list(backtest_results["total"].values))
    upper_values = (list(backtest_results["upper"].values))
    lower_values = (list(backtest_results["lower"].values))

    output = {

        "weights": {

            "labels": list(cleaned_weights.keys()),
            # Convert into percentages instead of proportions
            "data": [round(x * 100, 2) for x in list(cleaned_weights.values())]
        },

        "performance": {
            "labels": labels,
            "total": total_values,
            "upper": upper_values,
            "lower": lower_values
        },

        # TODO: Add more portfolio statistics : priority (3)
        "statistics": {
            "expected_return": performance[0],
            "volatility": performance[1],
            "sharpe_ratio": performance[2]
        }
    }

    return output


def min_volatility(parameters):

    print("Optimizer received: ", parameters)

    stocks_df = get_data(parameters["ticker_list"], datetime.strptime(parameters["start_date"], '%Y-%m-%d'),
                         datetime.strptime(parameters["end_date"], '%Y-%m-%d'))

    mu = expected_returns.mean_historical_return(stocks_df)
    S = risk_models.sample_cov(stocks_df)
    ef = EfficientFrontier(mu, S, weight_bounds=(0, 1))

    raw_weights = ef.min_volatility()
    cleaned_weights = ef.clean_weights()

    cleaned_weights = {k: v for k, v in cleaned_weights.items() if v != 0}

    # get tuple of 3 values: (return, vol, sharpe)
    performance = ef.portfolio_performance()

    backtest_results = backtest_portfolio(prices_df=stocks_df, portfolio=cleaned_weights,
                                          initial_amount=int(parameters["initial_amount"]), window=50)

    labels = (list(backtest_results["total"].index))

    total_values = (list(backtest_results["total"].values))
    upper_values = (list(backtest_results["upper"].values))
    lower_values = (list(backtest_results["lower"].values))

    output = {

        "weights": {

            "labels": list(cleaned_weights.keys()),
            # Convert into percentages instead of proportions
            "data": [round(x * 100, 2) for x in list(cleaned_weights.values())]
        },

        "performance": {
            "labels": labels,
            "total": total_values,
            "upper": upper_values,
            "lower": lower_values
        },

        # TODO: Add more portfolio statistics : priority (3)
        "statistics": {
            "expected_return": performance[0],
            "volatility": performance[1],
            "sharpe_ratio": performance[2]
        }
    }

    return output


def min_volatility_target(parameters):

    print("Optimizer received: ", parameters)

    target_return = float(
        parameters["optimization_parameters"]["target_return"])

    stocks_df = get_data(parameters["ticker_list"], datetime.strptime(parameters["start_date"], '%Y-%m-%d'),
                         datetime.strptime(parameters["end_date"], '%Y-%m-%d'))

    mu = expected_returns.mean_historical_return(stocks_df)
    S = risk_models.sample_cov(stocks_df)
    ef = EfficientFrontier(mu, S, weight_bounds=(0, 1))

    # Check documentation for parameters explanation
    raw_weights = ef.efficient_return(target_return, market_neutral=False)
    cleaned_weights = ef.clean_weights()

    cleaned_weights = {k: v for k, v in cleaned_weights.items() if v != 0}

    # get tuple of 3 values: (return, vol, sharpe)
    performance = ef.portfolio_performance()

    backtest_results = backtest_portfolio(prices_df=stocks_df, portfolio=cleaned_weights,
                                          initial_amount=int(parameters["initial_amount"]), window=50)

    labels = (list(backtest_results["total"].index))

    total_values = (list(backtest_results["total"].values))
    upper_values = (list(backtest_results["upper"].values))
    lower_values = (list(backtest_results["lower"].values))

    output = {

        "weights": {

            "labels": list(cleaned_weights.keys()),
            # Convert into percentages instead of proportions
            "data": [round(x * 100, 2) for x in list(cleaned_weights.values())]
        },

        "performance": {
            "labels": labels,
            "total": total_values,
            "upper": upper_values,
            "lower": lower_values
        },

        # TODO: Add more portfolio statistics : priority (3)
        "statistics": {
            "expected_return": performance[0],
            "volatility": performance[1],
            "sharpe_ratio": performance[2]
        }
    }

    return output


def max_return_target(parameters):

    print("Optimizer received: ", parameters)

    target_volatility = float(
        parameters["optimization_parameters"]["target_volatility"])

    stocks_df = get_data(parameters["ticker_list"], datetime.strptime(parameters["start_date"], '%Y-%m-%d'),
                         datetime.strptime(parameters["end_date"], '%Y-%m-%d'))

    mu = expected_returns.mean_historical_return(stocks_df)
    S = risk_models.sample_cov(stocks_df)
    ef = EfficientFrontier(mu, S, weight_bounds=(0, 1))

    # Check documentation for parameters explanation
    raw_weights = ef.efficient_risk(
        target_volatility, risk_free_rate=0.02, market_neutral=False)
    cleaned_weights = ef.clean_weights()

    cleaned_weights = {k: v for k, v in cleaned_weights.items() if v != 0}

    # get tuple of 3 values: (return, vol, sharpe)
    performance = ef.portfolio_performance()

    backtest_results = backtest_portfolio(prices_df=stocks_df, portfolio=cleaned_weights,
                                          initial_amount=int(parameters["initial_amount"]), window=50)

    labels = (list(backtest_results["total"].index))

    total_values = (list(backtest_results["total"].values))
    upper_values = (list(backtest_results["upper"].values))
    lower_values = (list(backtest_results["lower"].values))

    output = {

        "weights": {

            "labels": list(cleaned_weights.keys()),
            # Convert into percentages instead of proportions
            "data": [round(x * 100, 2) for x in list(cleaned_weights.values())]
        },

        "performance": {
            "labels": labels,
            "total": total_values,
            "upper": upper_values,
            "lower": lower_values
        },

        # TODO: Add more portfolio statistics : priority (3)
        "statistics": {
            "expected_return": performance[0],
            "volatility": performance[1],
            "sharpe_ratio": performance[2]
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

    # get tuple of 3 values: (return, vol, sharpe)
    performance = ef.portfolio_performance()

    # cleaned_weights = {k: round(v * 100, 3) for k, v in cleaned_weights.items() if v != 0}
    cleaned_weights = {k: v for k, v in cleaned_weights.items() if v != 0}

    backtest_results = backtest_portfolio(prices_df=stocks_df, portfolio=cleaned_weights, initial_amount=parameters[
                                          "initial_amount"], window=50)

    labels = (list(backtest_results["total"].index))

    total_values = (list(backtest_results["total"].values))
    upper_values = (list(backtest_results["upper"].values))
    lower_values = (list(backtest_results["lower"].values))

    output = {

        "weights": {

            "labels": list(cleaned_weights.keys()),
            # Convert into percentages instead of proportions
            "data": [round(x * 100, 2) for x in list(cleaned_weights.values())]
        },

        "performance": {
            "labels": labels,
            "total": total_values,
            "upper": upper_values,
            "lower": lower_values
        },

        # TODO: Add more portfolio statistics : priority (3)
        "statistics": {
            "expected_return": performance[0],
            "volatility": performance[1],
            "sharpe_ratio": performance[2]
        }
    }

    return output
