
import pandas as pd
import scipy.signal as signal
import sys

base_currency = sys.argv[1]
term_currency = sys.argv[2]


# Buterworth filter
N  = 2    # Filter order
Wn = 0.1 # Cutoff frequency
B, A = signal.butter(N, Wn, output='ba')
 
# Apply the filter

base = pd.read_csv('db/index/'+base_currency+'.csv')
base[base_currency] = round(base[base_currency].cumsum(),2)
base[base_currency+'f'] = signal.filtfilt(B,A, base[base_currency])

term = pd.read_csv('db/index/'+term_currency+'.csv')
term[term_currency] = round(term[term_currency].cumsum(),2)
term[term_currency+'f'] = signal.filtfilt(B,A, term[term_currency])

data = pd.merge(base,term, on=['date','date'])


trend = 0
trend_base = 0; trend_term = 0
last_basef = 0; last_termf = 0
for index, row in data.iterrows():

    if   row[base_currency+'f'] > last_basef: trend_base = 1
    elif row[base_currency+'f'] < last_basef: trend_base = -1
    else: trend_base = 0
    last_basef = row[base_currency+'f']

    if   row[term_currency+'f'] > last_termf: trend_term = 1
    elif row[term_currency+'f'] < last_termf: trend_term = -1
    else: trend_term = 0
    last_term = row[term_currency+'f']

    if   trend_base > 0 and trend_term < 0: trend = 1
    elif trend_base < 0 and trend_term > 0: trend = -1
    else: trend = 0

    print(row['date'], trend)



pd.options.plotting.backend = "plotly"
plt = data.plot(x='date', y=[base_currency, base_currency+'f', term_currency, term_currency+'f'])
plt.show()

