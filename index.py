
import pandas as pd

currencies = ['AUD','CAD','CHF','EUR','GBP','HKD','JPY','NZD','SGD','USD']

df = pd.read_csv('db/index/'+currencies[0]+'.csv')
df[currencies[0]] = df[currencies[0]].cumsum()
for i in range(1,len(currencies)):
    df2 = pd.read_csv('db/index/'+currencies[i]+'.csv')
    df2[currencies[i]] = df2[currencies[i]].cumsum()
    df = pd.merge(df,df2, on=['date','date'])

df = df.fillna(0)

pd.options.plotting.backend = "plotly"

plt = df.plot(x='date', y=currencies)
plt.show()



df = df.fillna(0)
df = df.set_index('date')


