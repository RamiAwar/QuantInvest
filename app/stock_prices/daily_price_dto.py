class DailyPriceDto:
    def __init__(self, stock_ticker, price, date):
        self.stock_ticker = stock_ticker
        self.price = price
        self.date = date

    def to_dict(self):
        data = {
            'stock_ticker': self.stock_ticker,
            'date': self.date,
            'price': self.price
        }
        return data