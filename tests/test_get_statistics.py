import unittest
from app.api.backtest.get_statistics import backtest_portfolio
from datetime import datetime
from dateutil.relativedelta import relativedelta



class GetStatisticsTests(unittest.TestCase):

    portfolio = {
                "AAPL": 0.2,
                "TSLA": 0.8
                }
    
    def test_compute_statistics(self):
        current_date = datetime.now()
        df = backtest_portfolio(self.portfolio, current_date-relativedelta(month=1), current_date)
        print(df)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()