"""
CoinMarketCap USD Price History

  Print the CoinMarketCap USD price history for a particular cryptocurrency in CSV format.
"""
from cmc.utils import utils

import pandas as pd
import argparse
import os

#----------------------------------------------------- Endpoints -----------------------------------------------------------

def getDataFor(cryptocurrencies, start_date, end_date, fields = [], asynchro = False, DOWNLOAD_DIR = None):
    if DOWNLOAD_DIR is not None:
        save =True
        if not os.path.exists(DOWNLOAD_DIR): os.makedirs(DOWNLOAD_DIR)
    else:
        save = False

    if not isinstance(cryptocurrencies, list): cryptocurrencies = [cryptocurrencies]

    all_cryptocurrencies = [currency.lower() for currency in cryptocurrencies]
    start_date, end_date = utils.parse_options(start_date, end_date)

    cryptocurrencies = []

    dfs = []
    # load cryptocurrencies from savepath
    if save:
        # first check if cryptocurrencies are saved in path
        for crypto in all_cryptocurrencies:

            filename = crypto + '_' + start_date + '_' + end_date + '.msg'
            path = os.path.join(DOWNLOAD_DIR, filename)
            if os.path.exists(path):
                print("Loading data for {} from {}".format(crypto, path))
                df = pd.read_msgpack(path)
                dfs.append(df)
            else:
                cryptocurrencies.append(crypto) # update list of cryptocurrencies to be scraped
    #otherwise, scrape all cryptos
    else:
        cryptocurrencies = all_cryptocurrencies

    if asynchro:
        # extract html asynchronously
        from cmc.asynchro import async_utils
        result_dict = async_utils.get_htmls(cryptocurrencies, start_date, end_date)
    else:
        # otherwise, extract data sequentially
        result_dict = utils.get_htmls(cryptocurrencies, start_date, end_date)

    # process html for each cryptocurrency
    for key in result_dict.keys():

        html = result_dict[key]
        header, rows = utils.extract_data(html)
        temp_df = pd.DataFrame(data = rows, columns = header)
        df = utils.processDataFrame(temp_df)

        if save:
            filename = key + '_' + start_date + '_' + end_date + '.msg'
            path = os.path.join(DOWNLOAD_DIR, filename)
            df.to_msgpack(path)

        dfs.append(df)

    # filter fields
    if len(fields) > 0: dfs = [df[fields] for df in dfs]

    return (pd.concat(dfs, axis = 1, keys = all_cryptocurrencies, join = 'outer'))

#------------------------------------------------ Command Line Args -----------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("currency",  help="This is the name of the crypto, as is shown on coinmarketcap. Optionally, enter a list of comma separated cryptocurrencies with no spaces in between."
                                        "i.e. bitcoin, ripple, ethereum, etc.", type=str)
parser.add_argument("start_date",help="Start date for which you wish to retrieve the historical data."                                         "Format is: yyyy-mm-dd. i.e. 2017-12-30 ", type=str)
parser.add_argument("end_date",    help="End date for the historical data retrieval. If you wish to retrieve all the "
                                        "data then you can give a date in the future. Same format as in start_date "
                                        "'yyyy-mm-dd'.", type=str)
parser.add_argument("--asyncro", help="If present, scrapes cryptocurrencies asynchronously (faster).", default = False,action='store_true')


#------------------------------------------------- Command Line Methods -------------------------------------------------------

def main(args=None):
    '''
    Interface for the command line application.
    '''
    if(args is not None):
        args = parser.parse_args(args)
    else:
        args = parser.parse_args()

    cryptocurrencies, start_date, end_date, asynchro = args.currency, args.start_date, args.end_date, args.asyncro

    cryptocurrencies = cryptocurrencies.split(',')

    df = getDataFor(cryptocurrencies, start_date, end_date, asynchro = asynchro)

    print(df.to_string())


# run CLI tool
if __name__ == '__main__':
    df = main()
