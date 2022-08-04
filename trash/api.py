
from tracemalloc import start
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
from datetime import timedelta, date, datetime
from pathlib import Path
from numpy import isnan
import pandas as pd
pd.options.plotting.backend = "plotly"
import plotly.express as px
from datetime import datetime
from datetime import timedelta
import pytz
import os

os.environ['TZ'] = "UTC"

# symbols

symbols = ['AUD_CAD', 'AUD_CHF', 'AUD_HKD', 'AUD_JPY', 'AUD_NZD', 'AUD_SGD', 'AUD_USD',
           'CAD_CHF', 'CAD_HKD', 'CAD_JPY', 'CAD_SGD', 'CHF_HKD', 'CHF_JPY', 'EUR_AUD',
           'EUR_CAD', 'EUR_CHF', 'EUR_GBP', 'EUR_HKD', 'EUR_JPY', 'EUR_NZD', 'EUR_SGD',
           'EUR_USD', 'GBP_AUD', 'GBP_CAD', 'GBP_CHF', 'GBP_HKD', 'GBP_JPY', 'GBP_NZD',
           'GBP_SGD', 'GBP_USD', 'HKD_JPY', 'NZD_CAD', 'NZD_CHF', 'NZD_HKD', 'NZD_JPY',
           'NZD_SGD', 'NZD_USD', 'SGD_CHF', 'SGD_HKD', 'SGD_JPY', 'USD_CAD', 'USD_CHF',
           'USD_HKD', 'USD_JPY', 'USD_SGD']  

# key 

_TOKEN = "37d11dc6e01ec900277bcf70ed296912-60827d532c22d5b1b0d3583a0e9309ef" 

# py api

api = API(access_token=TOKEN)

m = 10000

data = { 'datetime': [], 'alpha': [], 'beta': [], 'delta_p': [], 'delta_n': [], 'gamma': [], 'sigma': [], 'price': [] }

start_date = datetime.strptime('2010', '%Y')

# now_time = datetime.utcnow()-timedelta(minutes=4000)

to_date = datetime.utcnow()

while start_date < to_date:

    start_date = datetime.strftime(start_date, '%Y-%m-%dT%H:%M:%S') + '.000000000Z'
    print(start_date)

    params = { 'granularity': 'M1', 'from': start_date, 'count': 5000 }

    req = api.request(instruments.InstrumentsCandles('EUR_USD', params))

    #print(req['candles'][0]['time'][:19])
    #print(req['candles'][-1]['time'][:19])
    #print('\n')

    for mid in req['candles']:

        dt = datetime.strptime(mid['time'][:19], '%Y-%m-%dT%H:%M:%S')

        c = float(mid['mid']['c'])
        o = float(mid['mid']['o'])
        h = float(mid['mid']['h'])
        l = float(mid['mid']['l'])
        digits = len(mid['mid']['c'].split('.')[1])

        alpha = round((c/o-1)*m, 2)
        beta  = round((h/l-1)*m, 2)
        delta_p = 0
        delta_n = 0
        if alpha > 0:
            delta_p = round((o/l-1)*m, 2)
            delta_n = round((h/c-1)*m, 2)
        else:
            delta_p = round((c/l-1)*m, 2)
            delta_n = round((h/o-1)*m, 2)

        gamma = round(alpha + delta_p - delta_n, 2)
        sigma = 0 if alpha == 0 else round(beta/abs(alpha), 2)

        price = round((o+h+l+c+c)/5, digits)
        
        data['datetime'].append(dt)
        data['alpha'].append(alpha)
        data['beta'].append(beta)
        data['delta_p'].append(delta_p)
        data['delta_n'].append(delta_n)
        data['gamma'].append(gamma)
        data['sigma'].append(sigma)
        data['price'].append(price)

    start_date = data['datetime'][-1]

# dataframe

df = pd.DataFrame.from_dict(data).set_index('datetime')

df['month'] = df.index.month
df['day'] = df.index.day
df['weekday'] = df.index.weekday
df['hour'] = df.index.hour
df['minute'] = df.index.minute

df2 = df[df['alpha']<0]

px.histogram(x=df2['hour'], y=df2['alpha']).show()

df.corr()

df[['delta_p', 'delta_n']].corr() ** 2

from sklearn.metrics import r2_score

r2_score(df['delta_p'], df['delta_n'])

# rest_api

import json
import numpy as np
import pandas as pd
import requests

TOKEN = "" 

TRADING_ENVIRONMENTS = {
    "practice": {
        "stream": 'https://stream-fxpractice.oanda.com',
        "api": 'https://api-fxpractice.oanda.com'
    },
    "live": {
        "stream": 'https://stream-fxtrade.oanda.com',
        "api": 'https://api-fxtrade.oanda.com'
    }
}

start_date = ''
requests.get('https://api-fxpractice.oanda.com')

client = requests.Session()
client.headers['Authorization'] = 'Bearer '+ TOKEN
req = client.get('https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles?count=5000&price=BA&granularity=S5&from='+start_date).content.decode('utf-8')

req = json.loads(req)

data = pd.DataFrame.from_dict(req['candles'])

data['bid']

data.head

# end

