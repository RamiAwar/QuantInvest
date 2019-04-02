import pandas as pd

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

from app.api.stock_fetcher.get_data import get_data
from app.api.backtest import get_daily_returns

from datetime import datetime


def max_sharpe(parameters):

    print("From optimizer: ", parameters)

    stocks_df = get_data(parameters["ticker_list"], datetime.strptime(parameters["start_date"], '%Y-%m-%d'), 
                                    datetime.strptime(parameters["end_date"], '%Y-%m-%d'));

    

    mu = expected_returns.mean_historical_return(stocks_df)

    S = risk_models.sample_cov(stocks_df)

    ef = EfficientFrontier(mu, S, weight_bounds=(0, 1))

    raw_weights = ef.max_sharpe()

    cleaned_weights = ef.clean_weights()

    cleaned_weights = {k: round(v*100, 3) for k, v in cleaned_weights.items() if v != 0}

    backtest_results = get_daily_returns(cleaned_weights, parameters["start_date"], parameters["end_date"])

    print(backtest_results.head())
    # data = {}
    # data["labels"] = list(cleaned_weights.keys())
    # data["data"] = list(cleaned_weights.values())
    # data["performance"] = backtest_results

    # Testing data
    # data = {
    # 	"labels": ["AAPL", "AMZN", "TSLA"],
    # 	"data": [10, 80, 10]
    # }

    return cleaned_weights
