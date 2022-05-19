
# create a file named token.py with token = 'your_oanda_token'
import token 


from oandapyV20.contrib.factories import InstrumentsCandlesFactory
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import pandas as pd

access_token = token.token

client = API(access_token=access_token)

params = {
    "granularity": 'H1',
    "count": 3000
}


AUD = ['AUD_CAD','AUD_CHF','AUD_JPY','AUD_NZD']


r = instruments.InstrumentsCandles(instrument="EUR_USD",params=params)

r = client.request(r)

price = (float(r['candles'][0]['mid']['o'])+float(r['candles'][0]['mid']['h'])+float(r['candles'][0]['mid']['l'])+float(r['candles'][0]['mid']['c']))/4

