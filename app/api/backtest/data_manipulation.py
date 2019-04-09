import pandas as pd

def dict_to_dataframe(stock_prices_dict): # takes in a dictionary of stock prices and returns a dataframe
    list_of_earliest_dates = []
    list_of_oldest_dates = []

    for key, value in stock_prices_dict.items():
        list_of_earliest_dates.append(value[0]['date'])
        list_of_oldest_dates.append(value[-1]['date'])

    earliest_date = max(list_of_earliest_dates) # to get a common starting point for all stocks
    oldest_date = min(list_of_oldest_dates) # to get a common ending point for all stocks
    df = pd.DataFrame() # this will contain a column for each stock and be indexed by date
    df['date'] = pd.date_range(earliest_date, oldest_date)
    df = df.set_index(['date'])

    for key, value in stock_prices_dict.items():
        df[key] = float('nan')
        for stock_quote in value:
            current_date = stock_quote['date']
            if current_date < earliest_date or current_date > oldest_date:
                continue
            df.at[current_date, key] = stock_quote['price']
    return df        