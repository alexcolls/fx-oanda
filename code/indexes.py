from os import listdir
import pandas as pd
import scipy.signal as signal
from pathlib import Path


timeframes = [k for k in listdir('db/instruments/')]

currencies = ['AUD', 'CAD', 'CHF', 'EUR',
              'GBP', 'HKD', 'JPY', 'NZD', 'SGD', 'USD']


def index(currency, timeframe):
    files = [k for k in listdir('db/instruments/'+timeframe) if currency in k]
    df = pd.read_csv('db/instruments/'+timeframe+'/'+files[0])
    if files[0][0:3] != currency:
        df['return'] = -df['return']
    df = df.rename(columns={'return': files[0][0:7]})
    for i in range(1, len(files)):
        df2 = pd.read_csv('db/instruments/'+timeframe+'/'+files[i])
        if files[i][0:3] != currency:
            df2['return'] = -df2['return']
        df2 = df2.rename(columns={'return': files[i][0:7]})
        df = pd.merge(df, df2, on=['date', 'date'])
    df = df.fillna(0)
    df = df.set_index('date')
    df[currency] = round(df.sum(axis=1)/len(currencies), 2)
    df = df[currency]
    Path('db/indexes/raw/'+timeframe).mkdir(parents=True, exist_ok=True)
    df.to_csv('db/indexes/raw/'+timeframe+'/'+currency+'.csv', index=True)
    print(timeframe, currency, 'done')


for tf in timeframes:
    for curr in currencies:
        index(curr, tf)
