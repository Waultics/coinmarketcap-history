from cmc import coinmarketcap
import unittest
from datetime import datetime

class TestHistoricalData(unittest.TestCase):
  def test_data_gathered(self):
    cryptos = ['bitcoin']
    start_date, end_date = datetime(2017,6,1), datetime(2018,6,1)
    df = coinmarketcap.getDataFor(cryptos, start_date, end_date)
    self.assertTrue(len(df) > 0)

if __name__=="__main__":
  unittest.main()
