
# create a file named key.py with token = 'your_oanda_token'
from key import key

from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import pandas as pd


client = API(access_token=key.token)


periods = 3000

params = {
    "granularity": 'H1',
    "count": periods
}


AUD = [ 'AUD_CAD','AUD_CHF','AUD_HKD','AUD_JPY','AUD_NZD','AUD_SGD','AUD_USD',
        'CAD_CHF','CAD_HKD','CAP_JPY','CAD_SGD','CHF_HKD','CHF_JPY','EUR_AUD',
        'EUR_CAD' ]




def index( currency, symbols ):
    for sym in symbols:
        for i in range(periods):
            date = r['candles'][0]['time'][0:10]
            hour = int(r['candles'][13]['time'][11:13])
            price = (float(r['candles'][0]['mid']['o'])+float(r['candles'][0]['mid']['h'])+float(r['candles'][0]['mid']['l'])+float(r['candles'][0]['mid']['c']))/4
            if inverse:
                price = 1/price
            price = round(price,6)
