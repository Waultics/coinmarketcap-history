CoinMarketCap history scraper
=============================

Print the [CoinMarketCap](http://www.coinmarketcap.com) [USD price history](https://coinmarketcap.com/currencies/bitcoin/historical-data/) for a particular cryptocurrency in CSV format.

Among other things, this is useful for US tax reporting.  If you want to know the cost basis for a trade (or for coins acquired through mining), the IRS requires you to denominate that cost basis in USD.  In the case of token-for-token trades (e.g. purchasing ETH with BTC), that requires you know the USD:BTC exchange rate at the time of the trade.

Surprisingly, as of October 2017, it's not easy to get this data in a machine-readable format anywhere online.

Rather than getting the exchange rate at the exact moment of your trade, which is generally not feasible, the IRS standard (at least for similar situations w/stock) is to use the average of a stock's high and low price for the day. CoinMarketCap doesn't provide this figure, but this tool calculates this number and includes it in the output.

**Installation:**

This script requires Python 2 to be available at /usr/bin/python.  This is the case by default with macOS.

**Usage:**
 
```
./coinmarketcap-usd-history.py <currency> <start_year> <end_year>
```

**Where:**

* `<currency>` is the (case-insensitive) name of the currency / token as displayed on CoinMarketCap, with dashes in place of spaces
* `<start_year>` is the beginning of the range to fetch data for
* `<end_year>` is the end of the range to fetch data for

The above information can also be found by running: `python coinmarketcap-usd-history.py -h` in your terminal.

You can, of course, write results to a file with output redirection:

```
./coinmarketcap-usd-history.py <currency> <start_year> <end_year> > <output_filename>
```
