
import pandas as pd
import scipy.signal as signal
from os import listdir
import sys


# buterworth filter parameters
N = 2  # filter order
Wn = 0.3  # cutoff frequency
B, A = signal.butter(N, Wn, output='ba')


def LowPass(B, A, Currency):
    # get currency index from db
    df = pd.read_csv('db/index/'+Currency+'.csv')
    # cumulative sum to create trend
    df[Currency] = round(df[Currency].cumsum(), 2)
    # apply lowpass filter
    df[Currency+'f'] = signal.filtfilt(B, A, df[Currency])
    return df


currencies = ['AUD', 'CAD', 'CHF', 'EUR',
              'GBP', 'HKD', 'JPY', 'NZD', 'SGD', 'USD']

files = [k for k in listdir('db/pairs') if currency in k]


# create signal
trend_base = 0
trend_term = 0
last_basef = 0
last_termf = 0
signal = 0
signal_slow = 0
alpha = 0


for index, row in data.iterrows():

    if row[base_currency+'f'] > last_basef:
        trend_base = 1
    elif row[base_currency+'f'] < last_basef:
        trend_base = -1
    else:
        trend_base = 0
    last_basef = row[base_currency+'f']

    if row[term_currency+'f'] > last_termf:
        trend_term = 1
    elif row[term_currency+'f'] < last_termf:
        trend_term = -1
    else:
        trend_term = 0
    last_term = row[term_currency+'f']

    trend = trend_base + trend_term

    if row[base_currency] > row[base_currency+'f'] and row[term_currency] < row[term_currency+'f']:
        signal = -1
    elif row[base_currency] < row[base_currency+'f'] and row[term_currency] > row[term_currency+'f']:
        signal = 1
    else:
        signal = 0

    alpha = trend + signal
    print(row['date'], alpha)


matrix = df.corr()
hm = sns.heatmap(matrix, annot=True)
hm.set(title="FX G10 Correlation Matrix\n")
plt.show()
