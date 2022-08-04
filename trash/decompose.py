from re import S
from statsmodels.tsa.seasonal import seasonal_decompose
import pandas as pd

symbol = 'EUR'

data = pd.read_csv('db/indexes/raw/D/'+symbol+'.csv')
data[symbol] = data[symbol].cumsum()
data = data.set_index('date')


result = seasonal_decompose(
    data[symbol], model='additive', extrapolate_trend='freq', period=1)
plt = result.plot()
plt.show()
