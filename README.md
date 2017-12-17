CoinMarketCap history scraper
=============================

Print the [CoinMarketCap](http://www.coinmarketcap.com) [USD price history](https://coinmarketcap.com/currencies/bitcoin/historical-data/) for a particular cryptocurrency in CSV format.

Among other things, this is useful for US tax reporting.  If you want to know the cost basis for a trade (or for coins acquired through mining), the IRS requires you to denominate that cost basis in USD.  In the case of token-for-token trades (e.g. purchasing ETH with BTC), that requires you know the USD:BTC exchange rate at the time of the trade.

Surprisingly, as of October 2017, it's not easy to get this data in a machine-readable format anywhere online.

Rather than getting the exchange rate at the exact moment of your trade, which is generally not feasible, the IRS standard (at least for similar situations w/stock) is to use the average of a stock's high and low price for the day. CoinMarketCap doesn't provide this figure, but this tool calculates this number and includes it in the output.

## Installation

This script requires Python 2 to be available at /usr/bin/python.  This is the case by default with macOS.

## Usage

Just run in the terminal:
```shell
./coinmarketcap_usd_history.py <currency> <start_date> <end_date>
```
   
where

* `currency` is the (case-insensitive) name of the currency / token as displayed on CoinMarketCap, with dashes in place of spaces
* `start_date` is the beginning of the range to fetch data for. For example, 2017-10-01 (for 2017 October 10th)
* `end_year` is the end of the range to fetch data for. You may use the date in the future here to obtain the latest data. Format is the same as in the start date.

The above information can also be found by running: `python coinmarketcap_usd_history.py -h` in your terminal.

You can, of course, write the results to a file with the output redirection:

```shell
./coinmarketcap_usd_history.py <currency> <start_date> <end_date> > <output_filename>
```

#### Example
```shell
python coinmarketcap_usd_history.py bitcoin 2017-01-01 2017-12-31 > testfile
```

## Usage in another python module

You can also use `coinmarketcap.py` as a module in other python modules to get back a pandas dataframe with a cryptocurrency's history. 

First, you may need to add the path to `coinmarketcap_usd_history.py` in your `sys.path` through a command like the following:  

```python
sys.path.append(<path_to_coinmarketcap_usd_history.py_parent_folder>)
```

(Alternatively, just move the `coinmarketcap_usd_history.py` file to the directory of the including module.)

Second, import the module: 

```import coinmarketcap_usd_history```

Finally perform this to obtain the dataframe:

```python
df = coinmarketcap_usd_history.main(['bitcoin','2017-01-01','2017-12-31','--dataframe'])
```

If you just wish to have the CSV output returned as a string to another python module, simply omit the `'--dataframe'` parameter.
