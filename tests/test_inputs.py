from cmc import coinmarketcap
from cmc.utils import utils
import unittest
from datetime import datetime

class TestInputs(unittest.TestCase):
  def test_fake_crypto(self):
    cryptos = ['blah_crypto']
    start_date, end_date = datetime(2017,6,1), datetime(2018,6,1)
    with self.assertRaises(SystemExit):
      coinmarketcap.getDataFor(cryptos, start_date, end_date)

  def test_date_parser_invalid_date(self):
      # expect data %Y-%m-%d
      start = "2017-05-05"
      end = "2018-3-3"

      with self.assertRaises(ValueError):
         utils.parse_options(start, end)

if __name__=="__main__":
  unittest.main()
