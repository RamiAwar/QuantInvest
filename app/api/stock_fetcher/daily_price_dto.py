class DailyPriceDto:

    def __init__(self, ticker, price, date):
        self.ticker = ticker
        self.price = price
        self.date = date

    def to_dict(self):
        data = {
            'ticker': self.ticker,
            'date': self.date,
            'price': self.price
        }
        return data