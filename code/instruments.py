
# create a file named key.py with token = 'your_oanda_token' in the key folder
from key import key

from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
from os import listdir
import pandas as pd
from pathlib import Path
import sys

client = API(access_token=key.token)

# pairs to request to oanda
symbols = ['AUD_CAD', 'AUD_CHF', 'AUD_HKD', 'AUD_JPY', 'AUD_NZD', 'AUD_SGD', 'AUD_USD',
           'CAD_CHF', 'CAD_HKD', 'CAD_JPY', 'CAD_SGD', 'CHF_HKD', 'CHF_JPY', 'EUR_AUD',
           'EUR_CAD', 'EUR_CHF', 'EUR_GBP', 'EUR_HKD', 'EUR_JPY', 'EUR_NZD', 'EUR_SGD',
           'EUR_USD', 'GBP_AUD', 'GBP_CAD', 'GBP_CHF', 'GBP_HKD', 'GBP_JPY', 'GBP_NZD',
           'GBP_SGD', 'GBP_USD', 'HKD_JPY', 'NZD_CAD', 'NZD_CHF', 'NZD_HKD', 'NZD_JPY',
           'NZD_SGD', 'NZD_USD', 'SGD_CHF', 'SGD_HKD', 'SGD_JPY', 'USD_CAD', 'USD_CHF',
           'USD_HKD', 'USD_JPY', 'USD_SGD']

timeframe = str(sys.argv[1])  # input 1
periods = int(sys.argv[2])  # input 2

path = 'db/instruments'

# oanda params
params = {
    'granularity': timeframe,
    'count': periods
}


def db(symbols):
    for sym in symbols:
        print('Downloading '+sym+'...')
        r = instruments.InstrumentsCandles(sym, params)
        r = client.request(r)
        date = r['candles'][0]['time'][0:19]
        ret = 0
        vol = 0
        df = pd.DataFrame({'date': date, 'return': ret,
                          'volatility': vol}, index=[0])
        for i in range(1, len(r['candles'])):
            date = r['candles'][i]['time'][0:19]
            ret = round((float(r['candles'][i]['mid']['c']) /
                         float(r['candles'][i]['mid']['o'])-1)*100, 2)
            vol = round((float(r['candles'][i]['mid']['h']) /
                        float(r['candles'][i]['mid']['l'])-1)*100, 2)
            add = pd.DataFrame(
                {'date': date, 'return': ret, 'volatility': vol}, index=[0])
            df = pd.concat([df, add], ignore_index=True)

        Path(path+'/'+timeframe).mkdir(parents=True, exist_ok=True)
        df.to_csv(path+'/'+timeframe+'/'+sym+'.csv', index=False)


if __name__ == '__main__':
    db(symbols)
    print('db: '+timeframe+' history updated!')
