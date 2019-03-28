import pandas as pd

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

from app.api.stock_prices.get_data import get_all_snp500_data

from datetime import datetime

def efficient_risk_volatility(parameters):

	print("From optimizer: ", parameters)

	start = datetime(year=int(float(parameters["time_range"][0])), month=1, day=1)
	end = datetime(year=int(float(parameters["time_range"][1])), month=1, day=1)

	snp500_df = get_historical_data(tickers[:100], start=start, end=end, output_format="pandas")
	snp500_df = pd.concat([snp500_df[stock]["open"] for stock in tickers[:100]], axis=1, keys=tickers[:100])


	mu = expected_returns.mean_historical_return(snp500_df)

	S = risk_models.sample_cov(snp500_df)


	ef = EfficientFrontier(mu, S, weight_bounds=(0, 1))
	
	raw_weights = ef.max_sharpe()

	cleaned_weights = ef.clean_weights()

	cleaned_weights = {k: v for k, v in cleaned_weights.items() if v != 0}

	return cleaned_weights