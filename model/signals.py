
import pandas as pd
from os import listdir
import scipy.signal as signal


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


currencies = ['AUD', 'CAD', 'CHF', 'EUR',
              'GBP', 'HKD', 'JPY', 'NZD', 'SGD', 'USD']

files = [k for k in listdir('db/pairs')]

for file in files:

    x = file[0:3]  # base name
    y = file[4:7]  # term name

    base = LowPass(x)
    term = LowPass(y)
    # merge two currencies
    data = pd.merge(base, term, on=['date', 'date'])
    data = data.set_index('date')
    print(data)

    # base (x), term (y)
    x0f = 0  #
    y0f = 0  # current lowpass filter value
    x1f = 0  #
    y1f = 0  # last lowpass filter value
    xt = 0  #
    yt = 0  # trend indicator
    sig = 0  # signal

    df = pd.DataFrame(columns=['date', 'trend', 'signal'])

    for index, row in data.iterrows():
        # base trend indicator
        x0f = row[x+'f']
        if x0f > x1f:
            xt = 1
        elif x0f < x1f:
            xt = -1
        else:
            xt = 0
        x1f = x0f

        # term trend indicator
        y0f = row[y+'f']
        if y0f > y1f:
            yt = 1
        elif y0f < y1f:
            yt = -1
        else:
            yt = 0
        y1f = y0f

        # pair trend
        trend = xt - yt

        # signal
        if row[x] > x0f and row[y] < y0f:
            sig = -1
        elif row[x] < x0f and row[y] > y0f:
            sig = 1
        else:
            sig = 0

        # append to dataframe
        df.loc[len(df.index)] = [index, trend, sig]

    df.to_csv('db/signals/'+file, index=False)
