import urllib.request as urllib
import datetime
import sys
import pandas as pd
import re

# check if in jupyter notebook
def is_interactive():
    import __main__ as main
    return not hasattr(main, '__file__')

#------------------------------------------------- Utility Methods -------------------------------------------------------

def parse_options(start_date, end_date):
    '''
    Extract and filter parameters from command line.
    '''

    # convert date to string from datetime object
    if not isinstance(start_date, str): start_date = start_date.strftime("%Y-%m-%d")
    if not isinstance(end_date, str): end_date   = end_date.strftime("%Y-%m-%d")

    start_date_split = start_date.split('-')
    end_date_split   = end_date.split('-')

    start_year = int(start_date_split[0])
    end_year   = int(end_date_split[0])

    # String validation
    pattern    = re.compile('[2][0][1][0-9]-[0-1][0-9]-[0-3][0-9]')
    if not re.match(pattern, start_date):
        raise ValueError('Invalid format for the start_date: ' + start_date + ". Should be of the form: yyyy-mm-dd.")
    if not re.match(pattern, end_date):
        raise ValueError('Invalid format for the end_date: '   + end_date   + ". Should be of the form: yyyy-mm-dd.")
    # Datetime validation for the correctness of the date. Will throw a ValueError if not valid
    datetime.datetime(start_year,int(start_date_split[1]),int(start_date_split[2]))
    datetime.datetime(end_year,  int(end_date_split[1]),  int(end_date_split[2]))

    # CoinMarketCap's price data (at least for Bitcoin, presuambly for all others) only goes back to 2013
    invalid_args =                 start_year < 2013
    invalid_args = invalid_args or end_year   < 2013
    invalid_args = invalid_args or end_year   < start_year

    if invalid_args:
        print('Usage: ' + __file__ + ' <currency> <start_date> <end_date> --dataframe')
        sys.exit(1)

    start_date = start_date_split[0]+ start_date_split[1] + start_date_split[2]
    end_date   = end_date_split[0]  + end_date_split[1]   + end_date_split[2]

    return start_date, end_date



def craft_url(cryptocurrency, start_date, end_date):
    """
    Constructs the coinmarketcap url for the specified cryptocurrency, start date, and end date

    params
    ---------
    cryptocurrency: String
        * The cryptocurrency to construct URL for
    start_date: String
        * The start date for data collection. String should be in yyyy-mm-dd format
    end_date: String
        * The end date for data collection. String should be in yyyy-mm-dd format

    output
    --------
    url: String
        * url to access when scraping data
    """

    url = 'https://coinmarketcap.com/currencies/' + cryptocurrency + '/historical-data/' + '?start=' \
                                                + start_date + '&end=' + end_date

    return url

def extract_data(html):
    """
    Extract the price history from the HTML.

    The CoinMarketCap historical data page has just one HTML table.  This table contains the data we want.
    It's got one header row with the column names.

    We need to derive the "average" price for the provided data.

    params
    --------
    html
        * Raw html to extract historical data from

    outputs
    --------
    header: list
        * list of the headers provided by coinmarketcap
    rows: list
        * list of the row(s) for each header value.
    """
    # read table headers
    head = re.search(r'<thead>(.*)</thead>', html.decode('utf-8'), re.DOTALL).group(1)
    # find all values in table header
    header = re.findall(r'<th .*>([\w /*]+)</th>', head)
    # append 'Average' column to headers. This contains the average of the low and high prices for the day.
    header.append('Average')
    header = [s.replace('*', '') for s in header]

    # get all rows from the html page
    body = re.search(r'<tbody>(.*)</tbody>', html.decode('utf-8'), re.DOTALL).group(1)
    raw_rows = re.findall(r'<tr[^>]*>' + r'\s*<td[^>]*>([^<]+)</td>'*7 + r'\s*</tr>', body)

    # strip commas
    rows = []
    for row in raw_rows:
        row = [ field.replace(',','') for field in row ]
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

def processDataFrame(df):
    '''
    Sort and replace empty fields in the pandas dataframe.
    '''
    assert isinstance(df, pd.DataFrame), "df is not a pandas DataFrame."

    cols = list(df.columns.values)
    cols.remove('Date')
    df.loc[:,'Date'] = pd.to_datetime(df.Date)
    for col in cols: df.loc[:,col] = df[col].apply(lambda x: float(x) if x.replace('.','').isdigit() else float(0)) # check columns to see if value is a number.
    df = df.sort_values(by='Date').reset_index(drop=True) # sort values by data
    df['Date'] =  pd.to_datetime(df['Date'], format='%Y-%m-%d') # convert date index to datetime
    return df.set_index('Date')

def download_data(currency, start_date, end_date):
  """
  Download HTML price history for the specified cryptocurrency and time range from CoinMarketCap.
  """
  url = craft_url(currency, start_date, end_date)

  try:
    page = urllib.urlopen(url,timeout=10)
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

def get_htmls(cryptocurrencies, start_date, end_date):

    from tqdm import tqdm

    result_dict = {}
    # for progress bar
    cryptocurrencies = tqdm(cryptocurrencies)

    for crypto in cryptocurrencies:
        result_dict[crypto] = download_data(crypto, start_date, end_date)

    return result_dict
