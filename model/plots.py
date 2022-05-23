
import pandas as pd
import plotly.express as px
import seaborn as sns

currencies = ['AUD', 'CAD', 'CHF', 'EUR',
              'GBP', 'HKD', 'JPY', 'NZD', 'SGD', 'USD']

df = pd.read_csv('db/index/'+currencies[0]+'.csv')
df[currencies[0]] = df[currencies[0]].cumsum()
for i in range(1, len(currencies)):
    df2 = pd.read_csv('db/index/'+currencies[i]+'.csv')
    df2[currencies[i]] = df2[currencies[i]].cumsum()
    df = pd.merge(df, df2, on=['date', 'date'])

pd.options.plotting.backend = "plotly"
plt = df.plot(x='date', y=currencies)
plt.show()

matrix = round(df.corr(), 2)
fig = px.imshow(matrix, text_auto=True)
fig.show()

"""
matrix = df.corr()
hm = sns.heatmap(matrix, annot=True)
hm.set(title="FX G10 Correlation Matrix\n")
plt.show()
"""
