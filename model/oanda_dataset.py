
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
from datetime import timedelta, date, datetime
from pathlib import Path
from numpy import isnan
import pandas as pd
pd.options.plotting.backend = "plotly"
import plotly.express as px


# 
TOKEN = "37d11dc6e01ec900277bcf70ed296912-60827d532c22d5b1b0d3583a0e9309ef" # YOUR OANDA TOKEN
#
YEAR = 2021 # YEARS TO START



#

# instruments universe
symbols = ['AUD_CAD', 'AUD_CHF', 'AUD_HKD', 'AUD_JPY', 'AUD_NZD', 'AUD_SGD', 'AUD_USD',
           'CAD_CHF', 'CAD_HKD', 'CAD_JPY', 'CAD_SGD', 'CHF_HKD', 'CHF_JPY', 'EUR_AUD',
           'EUR_CAD', 'EUR_CHF', 'EUR_GBP', 'EUR_HKD', 'EUR_JPY', 'EUR_NZD', 'EUR_SGD',
           'EUR_USD', 'GBP_AUD', 'GBP_CAD', 'GBP_CHF', 'GBP_HKD', 'GBP_JPY', 'GBP_NZD',
           'GBP_SGD', 'GBP_USD', 'HKD_JPY', 'NZD_CAD', 'NZD_CHF', 'NZD_HKD', 'NZD_JPY',
           'NZD_SGD', 'NZD_USD', 'SGD_CHF', 'SGD_HKD', 'SGD_JPY', 'USD_CAD', 'USD_CHF',
           'USD_HKD', 'USD_JPY', 'USD_SGD']  

_from = str(YEAR)+'-01-01'
_to = str(YEAR)+'-12-31'


params = {'granularity': 'M1', 'from': _from, 'to': _to}
params = {'granularity': 'H12', 'count': 5000}

api = API(access_token=TOKEN)

req = api.request(instruments.InstrumentsCandles('AUD_JPY', params))


data = {'datetime': [], 'alpha': [], 'beta': [], 'delta_p': [], 'delta_n': [], 'gamma': [] }

for mid in req['candles']:

    d = datetime.strptime(mid['time'][:19], '%Y-%m-%dT%H:%M:%S')
    c = float(mid['mid']['c'])
    o = float(mid['mid']['o'])
    h = float(mid['mid']['h'])
    l = float(mid['mid']['l'])

    alpha = round((c/o-1)*10000, 2)
    beta  = round((h/l-1)*10000, 2)
    delta_p = 0
    delta_n = 0
    if alpha > 0:
        delta_p = round((o/l-1)*10000, 2)
        delta_n = round((h/c-1)*10000, 2)
    else:
        delta_p = round((c/l-1)*10000, 2)
        delta_n = round((h/o-1)*10000, 2)

    gamma = round(alpha + delta_p - delta_n, 2)
    
    data['datetime'].append(d)
    data['alpha'].append(alpha)
    data['beta'].append(beta)
    data['delta_p'].append(delta_p)
    data['delta_n'].append(delta_n)
    data['gamma'].append(gamma)

df = pd.DataFrame.from_dict(data).set_index('datetime')

df['month'] = df.index.month
df['day'] = df.index.day
df['weekday'] = df.index.weekday
df['hour'] = df.index.hour
df['minute'] = df.index.minute

px.histogram(x=df['month'], y=df['gamma'].abs()).show()

