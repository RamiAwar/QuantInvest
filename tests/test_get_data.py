import unittest
from app.api.stock_fetcher.get_data import get_data, get_all_snp500_data
from app.api.tasks import fetch_snp500_data
from datetime import datetime
from dateutil.relativedelta import relativedelta


class GetDataTests(unittest.TestCase):
    
    def test_get_data_multiple_stocks(self):
        current_date = datetime.now()
        data = get_data(['AAPL','TSLA'], current_date-relativedelta(month=1), current_date)
        self.assertTrue(True)

    def test_get_data_single_stock(self):
        current_date = datetime.now()
        get_data(['AAPL'], current_date-relativedelta(month=1), current_date)
        self.assertTrue(True)

    def test_get_all_snp500_data(self):
        current_date = datetime.now()
        df = get_all_snp500_data(current_date-relativedelta(months=11), current_date)
        print(df)
        self.assertFalse(df.isnull().values.any())
    
    def test_fetch_snp500_data(self):
        fetch_snp500_data(['AAPL','TSLA'])
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()