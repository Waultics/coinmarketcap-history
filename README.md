CoinMarketCap history scraper
=============================

Print the [CoinMarketCap](http://www.coinmarketcap.com) [USD price history](https://coinmarketcap.com/currencies/bitcoin/historical-data/) for a particular cryptocurrency in CSV format.

Among other things, this is useful for US tax reporting.  If you want to know the cost basis for a trade (or for coins acquired through mining), the IRS requires you to denominate that cost basis in USD.  In the case of token-for-token trades (e.g. purchasing ETH with BTC), that requires you know the USD:BTC exchange rate at the time of the trade.

Surprisingly, as of October 2017, it's not easy to get this data in a machine-readable format anywhere online.

Rather than getting the exchange rate at the exact moment of your trade, which is generally not feasible, the IRS standard (at least for similar situations w/stock) is to use the average of a stock's high and low price for the day. CoinMarketCap doesn't provide this figure, but this tool calculates this number and includes it in the output.

**Installation:**

This script requires Python 2 to be available at /usr/bin/python.  This is the case by default with macOS.

**Usage:**

Just run in the terminal:
```./coinmarketcap_usd_history.py <currency> <start_date> <end_date>```
   
**Where:**

* `<currency>` is the (case-insensitive) name of the currency / token as displayed on CoinMarketCap, with dashes in place of spaces
* `<start_date>` is the beginning of the range to fetch data for. For example, 2017-10-01 (for 2017 October 10th)
* `<end_year>` is the end of the range to fetch data for. You may use the date in the future here to obtain the latest data. Format is the same as in the start date.

The above information can also be found by running: `python coinmarketcap_usd_history.py -h` in your terminal.

You can, of course, write the results to a file with the output redirection:

```
./coinmarketcap_usd_history.py <currency> <start_date> <end_date> > <output_filename>
```
**Using in another python module:**

You can also use the module in other python modules to get back a pandas dataframe with the history of the crypto coin. You may need to add the path to `coinmarketcap_usd_history.py` in your `sys.path` through a command like the following: `sys.path.append(<path_to_coinmarketcap_usd_history.py_parent_folder>)` (alternatively, just move the `coinmarketcap_usd_history.py` file to the directory of your module that is to use `coinmarketcap_usd_history.py`). Also, import the module: `import coinmarketcap_usd_history`.Then perform this to obtain the dataframe: `df = coinmarketcap_usd_history.main(['bitcoin','2017','2017','--toDf'])`. Note that if you just wish to see the output of the call in another python module, simply omit the `'--toDf'` part, which acts as a boolean flag (i.e. if it is present, then it gets converted to `True`, otherwise `False`).
  
