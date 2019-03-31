import pandas as pd

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

from app.api.stock_fetcher.get_data import get_all_snp500_data
from app.api.backtest import get_daily_returns

from datetime import datetime



def efficient_risk_volatility(parameters):

	print("From optimizer: ", parameters)

	get_all_snp500_data(parameters["start_date"], parameters["end_date"])

	mu = expected_returns.mean_historical_return(snp500_df)

	S = risk_models.sample_cov(snp500_df)


	ef = EfficientFrontier(mu, S, weight_bounds=(0, 1))
	
	raw_weights = ef.max_sharpe()

	cleaned_weights = ef.clean_weights()

	cleaned_weights = {k: v for k, v in cleaned_weights.items() if v != 0}

	result = get_daily_returns(cleaned_weights, parameters["start_date"], parameters["end_date"])
	

	return [cleaned_weight, result]


