
# create a file named key.py with token = 'your_oanda_token'
from key import key

from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import pandas as pd

client = API(access_token=key.token)

syms = ['AUD_CAD','AUD_CHF','AUD_HKD','AUD_JPY','AUD_NZD','AUD_SGD','AUD_USD',
        'CAD_CHF','CAD_HKD','CAD_JPY','CAD_SGD','CHF_HKD','CHF_JPY','EUR_AUD',
        'EUR_CAD','EUR_CHF','EUR_GBP','EUR_HKD','EUR_JPY','EUR_NZD','EUR_SGD',
        'EUR_USD','GBP_AUD','GBP_CAD','GBP_CHF','GBP_HKD','GBP_JPY','GBP_NZD',
        'GBP_SGD','GBP_USD','HKD_JPY','NZD_CAD','NZD_CHF','NZD_HKD','NZD_JPY',
        'NZD_SGD','NZD_USD','SGD_CHF','SGD_HKD','SGD_JPY','USD_CAD','USD_CHF',
        'USD_HKD','USD_JPY','USD_SGD','XAG_AUD','XAG_CAD','XAG_CHF','XAG_EUR',
        'XAG_GBP','XAG_HKD','XAG_JPY','XAG_NZD','XAG_SGD','XAG_USD','XAU_AUD',
        'XAU_CAD','XAU_CHF','XAU_EUR','XAU_GBP','XAU_HKD','XAU_JPY','XAU_NZD',
        'XAU_SGD','XAU_USD','XAU_XAG']

periods = 5000

params = {
    'granularity': 'H1',
    'count': periods
}

def db( symbols ):
    for sym in symbols:
        print('\nDownloading '+sym+'...')
        r = instruments.InstrumentsCandles(sym,params)
        r = client.request(r)
        df = pd.DataFrame()
        for i in range(len(r['candles'])):
            date = r['candles'][i]['time'][0:19]
            #date = r['candles'][i]['time'][0:10]
            #hour = int(r['candles'][i]['time'][11:13])
            ret = round((float(r['candles'][i]['mid']['c'])/float(r['candles'][i]['mid']['o'])-1)*100, 2)
            #vol = round((float(r['candles'][i]['mid']['h'])/float(r['candles'][i]['mid']['l'])-1)*100, 2)
            add = pd.DataFrame({'date': date, 'return': ret}, index=[0])
            df = pd.concat([df, add], ignore_index=True)
        df.to_csv('db/'+sym+'.csv', index=False)
        
db(syms)


