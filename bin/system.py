
import key
import params

from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments

import pandas as pd
from os import listdir
import scipy.signal as signal
from time import sleep
from datetime import datetime


def db(symbols):

    client = API(access_token=key.token)
    _params = {'granularity': params.GRANULARITY, 'count': params.LOOKBACK}

    for sym in symbols:
        print('Downloading '+sym+'...')
        r = instruments.InstrumentsCandles(sym, _params)
        r = client.request(r)
        date = r['candles'][0]['time'][0:19]
        ret = 0
        df = pd.DataFrame({'date': date, 'return': round(ret, 2)}, index=[0])

        for i in range(1, len(r['candles'])):
            date = r['candles'][i]['time'][0:19]
            #date = r['candles'][i]['time'][0:10]
            #hour = int(r['candles'][i]['time'][11:13])
            ret = (float(r['candles'][i]['mid']['c']) /
                   float(r['candles'][i]['mid']['o'])-1)*100
            #vol = round((float(r['candles'][i]['mid']['h'])/float(r['candles'][i]['mid']['l'])-1)*100, 2)
            add = pd.DataFrame(
                {'date': date, 'return': round(ret, 2)}, index=[0])
            df = pd.concat([df, add], ignore_index=True)

        df.to_csv('db/pairs/'+sym+'.csv', index=False)


def index(currency):

    print('Creating '+currency+'...')
    files = [k for k in listdir('db/pairs') if currency in k]
    df = pd.read_csv('db/pairs/'+files[0])

    if files[0][0:3] != currency:
        df['return'] = -df['return']
    df = df.rename(columns={'return': files[0][0:7]})

    for i in range(1, len(files)):
        df2 = pd.read_csv('db/pairs/'+files[i])
        if files[i][0:3] != currency:
            df2['return'] = -df2['return']
        df2 = df2.rename(columns={'return': files[i][0:7]})
        df = pd.merge(df, df2, on=['date', 'date'])

    df = df.fillna(0)
    df = df.set_index('date')
    df[currency] = round(df.sum(axis=1)/len(params.indexes), 2)
    df = df[currency]
    df.to_csv('db/index/'+currency+'.csv', index=True)


def update_db():

    db(params.symbols)
    for curr in params.indexes:
        index(curr)
    print('db updated!')


def LowPass(currency):
    # buterworth filter parameters
    N = 2  # filter order
    Wn = 0.3  # cutoff frequency
    B, A = signal.butter(N, Wn, output='ba')
    # get currency index from db
    df = pd.read_csv('db/index/'+currency+'.csv')
    # cumulative sum to create trend
    df[currency] = round(df[currency].cumsum(), 2)
    # apply lowpass filter
    df[currency+'f'] = signal.filtfilt(B, A, df[currency])

    return df


files = [k for k in listdir('db/pairs')]

for file in files:

    x = file[0:3]  # base name
    y = file[4:7]  # term name

    base = LowPass(x)
    term = LowPass(y)
    # merge two currencies
    data = pd.merge(base, term, on=['date', 'date'])


def now():
    return datetime.now()


"""
while true:

    now
    sleep(60)
"""
