
# create a file named key.py with token = 'your_oanda_token'
from key import key

from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import pandas as pd

client = API(access_token=key.token)

periods = 5000

params = {
    'granularity': 'H1',
    'count': periods
}

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

sym='AUD_CAD'

def db( symbols ):
    for sym in symbols:
        print('\nDownloading '+sym+'...')
        r = instruments.InstrumentsCandles(sym,params)
        r = client.request(r)
        df = pd.DataFrame()
        for i in range(len(r['candles'])):
            index = r['candles'][i]['time'][0:19]
            date = r['candles'][i]['time'][0:10]
            hour = int(r['candles'][i]['time'][11:13])
            price = round( ( float(r['candles'][i]['mid']['o'])
                            +float(r['candles'][i]['mid']['h'])
                            +float(r['candles'][i]['mid']['l'])
                            +float(r['candles'][i]['mid']['c']))/4, 6 )
            add = pd.DataFrame({'date': date, 'hour': hour, 'price': price }, index=[0])
            df = pd.concat([df, add], ignore_index=True)
        df.to_csv('db/'+sym+'.csv', index=False)
        
db(syms)
