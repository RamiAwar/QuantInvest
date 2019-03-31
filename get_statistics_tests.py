import unittest
from app.api.backtest.get_statistics import prepare_dataframe, compute_statistics
from datetime import datetime
from dateutil.relativedelta import relativedelta



class GetStatisticsTests(unittest.TestCase):

    portfolio = {
                "AAPL": 0.2,
                "TSLA": 0.8
                }
    
    def test_compute_statistics(self):
        current_date = datetime.now()
        df = prepare_dataframe(self.portfolio, current_date-relativedelta(month=1), current_date)
        compute_statistics(df)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()