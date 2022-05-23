
import pandas as pd
import scipy.signal as signal
import sys

base_currency = sys.argv[1]
term_currency = sys.argv[2]


# Buterworth filter fast
N = 2  # Filter order
Wn = 0.3  # Cutoff frequency
Bf, Af = signal.butter(N, Wn, output='ba')

# Buterworth filter slow
N = 3  # Filter order
Wn = 0.1  # Cutoff frequency
Bs, As = signal.butter(N, Wn, output='ba')

# Apply the filter to base currency
base = pd.read_csv('index/'+base_currency+'.csv')
base[base_currency] = round(base[base_currency].cumsum(), 2)
# lowpass filter fast
base[base_currency+'f'] = signal.filtfilt(Bf, Af, base[base_currency])
# lowpass filter slow
base[base_currency+'s'] = signal.filtfilt(Bs, As, base[base_currency])

# Apply the filter to term currency
term = pd.read_csv('index/'+term_currency+'.csv')
term[term_currency] = round(term[term_currency].cumsum(), 2)
# lowpass filter fast
term[term_currency+'f'] = signal.filtfilt(Bf, Af, term[term_currency])
# lowpass filter slow
term[term_currency+'s'] = signal.filtfilt(Bs, As, term[term_currency])

# merge base and term
data = pd.merge(base, term, on=['date', 'date'])

pd.options.plotting.backend = "plotly"
# plt = data.plot(x='date', y=[base_currency, base_currency+'f',               base_currency+'s', term_currency, term_currency+'f', term_currency+'s'])

plt = data.plot(x='date', y=[
                base_currency, base_currency+'f', term_currency, term_currency+'f'])
plt.show()

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
