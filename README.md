# CoinMarketCap Historical Data Retrieval

Obtain [USD price history](https://coinmarketcap.com/currencies/bitcoin/historical-data/) data for [CoinMarketCap](http://www.coinmarketcap.com)-listed cryptocurrencies.

Use this library as a **command-line script** to obtain historical cryptocurrency data on the fly, or **import the `cmc` library** to obtain cryptocurrency data within your Python program.  

## Contents
* [Installation](#installation)
* [Usage](#usage)
  * [Command Line](#command-line)
    * [Usage](#command-line-usage)
    * [Examples](#command-line-examples)
  * [Module](#module)
    * [Usage](#library)
    * [Examples](#library-examples)
* [Legacy](#legacy)
* [Updates](#updates)
***

## Installation
Dependencies:
* asyncio
* aiohttp
* aiodns
* pandas
* tqdm

First install the required dependencies:
```shell
$ pip install asyncio aiohttp aiodns pandas tqdm
```

Then install coinmarketcap-history with pip:

```shell
$ pip install cmc
```

***

## Usage

### Command Line
The command line tool is useful for US tax reporting, among other things.  If you wish to report the cost basis for a trade (or for coins acquired through mining), the IRS requires you to denominate that cost basis in USD.  In the case of token-for-token trades (e.g. purchasing ETH with BTC), that requires you know the USD:BTC exchange rate at the time of the trade.

Rather than getting the exchange rate at the exact moment of your trade, which is generally not feasible, the IRS standard (at least for similar situations w/stock) is to use the average of a stock's high and low price for the day. CoinMarketCap doesn't provide this figure, but this tool does.

#### Command Line Usage

To gather cryptocurrency data, open a terminal and run:
```shell
$ coinmarketcap <currency1> <start_date> <end_date>
```
where:

* `currency` is the (case-insensitive) name of the currency / token as displayed on CoinMarketCap, with dashes in place of spaces (i.e. bitcoin).
* `start_date` is the beginning of the range to fetch data for in `yyyy-mm-dd` format (i.e. 2017-10-01 for 2017 October 10th).
* `end_year` is the end of the range to fetch data for in `yyyy-mm-dd` format.

Data for multiple cryptocurrencies can be obtained with:
```shell
$ coinmarketcap <currency_1,currency_2,...,currency_n> <start_date> <end_date>
```
**Note:** currencies must be comma-separated, with no spaces in between.

Data is returned in the following tabular format:


|          |Bitcoin   |          |          |          |          |          |          |
|----------|----------|----------|----------|----------|----------|----------|----------|
| Date     | Open     | High     |   Low    | Close    | Volume   |Market Cap| Average  |
|...       |...       |...       |...       |...       |...       |...       |...       |


The above information can also be found by running:
```shell
$ coinmarketcap -h
```

Write outputs to a file by running:

```shell
$ coinmarketcap <currency> <start_date> <end_date> > <output_filename>
```

For faster retrieval, cryptocurrency data can be gathered asynchronously by supplying the `--async` flag:

```shell
$ coinmarketcap <currency> <start_date> <end_date> --async
```

#### Command Line Examples
Collecting data for one cryptocurrency:
```shell
$ coinmarketcap bitcoin 2017-01-01 2017-12-31
```

Collecting data for multiple cryptocurrencies:
```shell
$ coinmarketcap bitcoin,ripple,ethereum 2017-01-01 2017-12-31
```

Collecting data for multiple cryptocurrencies asynchronously(faster):
```shell
$ coinmarketcap bitcoin,ripple,ethereum 2017-01-01 2017-12-31 --async
```

Writing output to a file:
```shell
$ coinmarketcap bitcoin 2017-01-01 2017-12-31 > bitcoin_history.csv
```

Writing output for multiple cryptocurrencies to a file:
```shell
$ python coinmarketcap.py bitcoin,ripple,ethereum 2017-01-01 2017-12-31 > bitcoin_ripple_ethereum_history.csv
```
***

### Module

In addition to command-line functionality, coinmarketcap-history provides the `cmc` library, which allows users to obtain CoinMarketCap data from within a Python program. Historical is returned in the form of a [Pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html), which allows for easy use.

#### Library

To get started with the `cmc` library, import it from within your program:

```python
from cmc import coinmarketcap
```

Data for cryptocurrencies can be gathered using the `getDataFor()` method:

##### getDataFor()
**params:**
  * `cryptocurrencies`: string or list
      * crypto(s) to be scraped. supply a string for a single cryptocurrency, or supply a list of strings for multiple cryptocurrencies.
  * `start_date`: datetime object
      * datetime object for the beginning of the range to fetch data for. Must contain values for year, month, and day.
  * `end_date`: datetime object
      * datetime object for the ebd of the range to fetch data for. Must contain values for year, month, and day.
  * `fields` **(optional)**: list
      * columns to obtain upon data retrieval. Options are:
          * ['Open','High','Low','Close','Volume','Market Cap','Average']
      * if `fields` is not specified, all fields are returned.
  * `async` **(optional)**: boolean
      * if `True`, data is gathered asynchronously. This is especially useful when gathering data for multiple cryptocurrencies at a time, which can be slow when gathered synchronously. If `async` is not specified, data is gathered synchronously.

  * `DOWNLOAD_DIR` **(optional)**: string
      * String of the relative path to save data to and load data from. If `DOWNLOAD_DIR` is not specified, no data is saved.

#### Library Examples
Gathering data for a single cryptocurrency:
```python
from cmc import coinmarketcap
from datetime import datetime

crypto = 'bitcoin'
start_date, end_date = datetime(2017,6,1), datetime(2018,6,1)

df_bitcoin = coinmarketcap.getDataFor(crypto, start_date, end_date)
```

Getting data for multiple cryptocurrencies:

```python
from cmc import coinmarketcap
from datetime import datetime

cryptos = ['bitcoin','ripple','ethereum']
start_date, end_date = datetime(2017,6,1), datetime(2018,6,1)

df_cryptos = coinmarketcap.getDataFor(cryptos, start_date, end_date)
```

To cache retrieved data, simply supply a string for `DOWNLOAD_DIR`. The string should be a relative path to the desired download directory. Data is stored in the lightweight `.msg` format.

Saving data and pulling cached data:
```Python
from cmc import coinmarketcap
from datetime import datetime

cryptos = ['bitcoin','ripple','ethereum']
start_date, end_date = datetime(2017,6,1), datetime(2018,6,1)

# retrieves data and stores .msg files in DOWNLOAD_DIR
df_cryptos = coinmarketcap.getDataFor(cryptos, start_date, end_date, DOWNLOAD_DIR = 'data/coinmarketcap')

# does not retreive data. Instead, pulls cached data from DOWNLOAD_DIR
df_cryptos = coinmarketcap.getDataFor(cryptos, start_date, end_date, DOWNLOAD_DIR = 'data/coinmarketcap')
```

Pulling specified columns only:
```python
from cmc import coinmarketcap
from datetime import datetime

cryptos = ['bitcoin','ripple','ethereum']
start_date, end_date = datetime(2017,6,1), datetime(2018,6,1)

df_cryptos = coinmarketcap.getDataFor(cryptos, start_date, end_date, fields = ['High','Low','Close'])
```
***

# Legacy

Legacy code can be obtained from the `coinmarketcap-history-legacy` repository found [here](https://github.com/Alescontrela/coinmarketcap-history-legacy).
***

# Updates

### 2.0.0 - July 6th, 2018
* as of version 2, coinmarketcap-history now offers support for Python 3. Additionally, the `cmc` artifact allows for global use of the `coinmarketcap` command line tool, as well as dedicated support for in-program operations.
