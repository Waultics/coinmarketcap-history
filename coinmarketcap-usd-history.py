#!/usr/bin/python

"""
CoinMarketCap USD Price History

  Print the CoinMarketCap USD price history for a particular cryptocurrency in CSV format.
"""

import sys
import re
import urllib2
import argparse

def parse_options(args):
  """
  Extract parameters from command line.
  """

  arg_currency   = args.currency.lower()
  arg_start_year = args.start_year
  arg_end_year   = args.end_year

  len_args = len(sys.argv[1:])
  invalid_args = len_args != 3

  if len_args >= 1: currency   = arg_currency
  if len_args >= 2: start_year = arg_start_year
  if len_args >= 3: end_year   = arg_end_year

  # CoinMarketCap's price data (at least for Bitcoin, presuambly for all others) only goes back to 2013
  invalid_args = invalid_args or int(start_year) < 2013
  invalid_args = invalid_args or int(end_year)   < 2013
  invalid_args = invalid_args or int(end_year)   < int(start_year)

  if invalid_args:
    print('Usage: ' + __file__ + ' <currency> <start_year> <end_year>');
    sys.exit(1)

  return currency, start_year, end_year


def download_data(currency, start_year, end_year):
  """
  Download HTML price history for the specified cryptocurrency and time range from CoinMarketCap.
  """

  start_date = start_year + '0101'
  end_date = end_year + '1231'
  url = 'https://coinmarketcap.com/currencies/' + currency + '/historical-data/' + '?start=' + start_date + '&end=' + end_date

  try:
    
    page = urllib2.urlopen(url,timeout=10)
    if page.getcode() != 200:
      raise Exception('Failed to load page') 
    html = page.read()
    page.close()

  except Exception as e:
    print('Error fetching price data from ' + url)
    print('Did you use a valid CoinMarketCap currency?\nIt should be entered exactly as displayed on CoinMarketCap.com (case-insensitive), with dashes in place of spaces.')
    
    if hasattr(e, 'message'):
	print("Error message: " + e.message)
    else:
	print(e)	
    sys.exit(1)

  return html


def extract_data(html):
  """
  Extract the price history from the HTML.

  The CoinMarketCap historical data page has just one HTML table.  This table contains the data we want.
  It's got one header row with the column names.

  We need to derive the "average" price for the provided data.
  """

  head = re.search(r'<thead>(.*)</thead>', html, re.DOTALL).group(1)
  header = re.findall(r'<th .*>([\w ]+)</th>', head)
  header.append('Average (High + Low / 2)')

  body = re.search(r'<tbody>(.*)</tbody>', html, re.DOTALL).group(1)
  raw_rows = re.findall(r'<tr[^>]*>\s*<td[^>]*>([^<]+)</td>\s*<td[^>]*>([^<]+)</td>\s*<td[^>]*>([^<]+)</td>\s*<td[^>]*>([^<]+)</td>\s*<td[^>]*>([^<]+)</td>\s*<td[^>]*>([^<]+)</td>\s*<td[^>]*>([^<]+)</td>\s*</tr>', body)

  # strip commas
  rows = []
  for row in raw_rows:
    row = [ field.translate(None, ',') for field in row ]
    rows.append(row)

  # calculate averages
  def append_average(row):
    high = float(row[header.index('High')])
    low = float(row[header.index('Low')])
    average = (high + low) / 2
    row.append( '{:.2f}'.format(average) )
    return row
  rows = [ append_average(row) for row in rows ]

  return header, rows


def render_csv_data(header, rows):
  """
  Render the data in CSV format.
  """
  print(','.join(header))

  for row in rows:
    print(','.join(row))

def initialize_arg_parser():
  # ----------- For user convenience. Shows required + optional parameters in the command line. ------------------------
  parser = argparse.ArgumentParser()
  parser.add_argument("currency", help="This is the name of the crypto, as is shown on coinmarketcap. For BTC, "
                                       "for example, type: bitcoin.", type=str)
  parser.add_argument("start_year", help="Start year from which you wish to retrieve historical data. Data will be "
                                         "retrieved from start_year-01-01 by default.", type=str)
  parser.add_argument("end_year", help="Last year (inclusive) for historical data retrieval. Data will be retrieved "
                                       "for up to end_year-31-12 by default.", type=str)

  args = parser.parse_args()

  print "** Arguments passed **"
  print "currency: %s"   % args.currency
  print "start_year: %s" % args.start_year
  print "end_year: %s"   % args.end_year

  return args
  # --------------------------------------------------------------------------------------------------------------------

def main():

  args = initialize_arg_parser()
  currency, start_year, end_year = parse_options(args)
  
  html = download_data(currency, start_year, end_year)
  header, rows = extract_data(html)
  render_csv_data(header, rows)

if __name__ == '__main__':
  main()
