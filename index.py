
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


currencies = ['AUD','CAD','CHF','EUR','GBP','HKD','JPY','NZD','SGD','USD']

PERIODS = int(sys.argv[1])

df = pd.read_csv('db/index/'+currencies[0]+'.csv')
df = df[-PERIODS:].reset_index().drop(columns='index')
df[currencies[0]] = df[currencies[0]].cumsum()
for i in range(1,len(currencies)):
    df2 = pd.read_csv('db/index/'+currencies[i]+'.csv')
    df = df[-PERIODS:].reset_index().drop(columns='index')
    df2[currencies[i]] = df2[currencies[i]].cumsum()
    df = pd.merge(df,df2, on=['date','date'])

pd.options.plotting.backend = "plotly"
plot = df.plot(x='date', y=currencies)
plot.show()

matrix = df.corr()
hm = sns.heatmap(matrix, annot = True)
hm.set(title = "FX G10 Correlation Matrix\n")
plt.show()


