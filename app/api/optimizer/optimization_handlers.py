import pandas as pd

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

from iexfinance.stocks import Stock
from iexfinance.stocks import get_historical_data

from datetime import datetime

def efficient_risk_volatility(parameters):

	print("From optimizer: ", parameters)

	start = datetime(year=int(float(parameters["time_range"][0])), month=1, day=1)
	end = datetime(year=int(float(parameters["time_range"][1])), month=1, day=1)

	# Stocks to fetch
	data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	table = data[0]

	tickers = table["Symbol"].tolist()

	snp500_df = get_historical_data(tickers[:100], start=start, end=end, output_format="pandas")
	snp500_df = pd.concat([snp500_df[stock]["open"] for stock in tickers[:100]], axis=1, keys=tickers[:100])


	mu = expected_returns.mean_historical_return(snp500_df)

	S = risk_models.sample_cov(snp500_df)


	ef = EfficientFrontier(mu, S, weight_bounds=(0, 1))
	
	raw_weights = ef.max_sharpe()

	cleaned_weights = ef.clean_weights()

	cleaned_weights = {k: round(v*100, 3) for k, v in cleaned_weights.items() if v != 0}

	data = {}
	data["labels"] = list(cleaned_weights.keys())
	data["data"] = list(cleaned_weights.values())

	# Testing data
	# data = {
	# 	"labels": ["AAPL", "AMZN", "TSLA"],
	# 	"data": [10, 80, 10]
	# }


	return data