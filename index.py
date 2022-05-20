from os import listdir
import pandas as pd

def index( currency ):
    print(currency+'...')
    files = [k for k in listdir('db') if currency in k]
    df = pd.read_csv('db/'+files[0])
    if files[0][0:3] != currency: df['return'] = -df['return']
    df = df.rename(columns={'return':files[0][0:7]})
    for i in range(1,len(files)):
        df2 = pd.read_csv('db/'+files[i])
        if files[i][0:3] != currency: df2['return'] = -df2['return']
        df2 = df2.rename(columns={'return':files[i][0:7]})
        df = pd.merge(df,df2, on=['date','date'])
    df = df.fillna(0)
    df = df.set_index('date')
    df[currency] = round(df.sum(axis=1),2)
    df = df[currency]
    df.to_csv('db/index/'+currency+'.csv', index=True)


currencies = ['AUD','CAD','CHF','EUR','GBP','HKD','JPY','NZD','SGD','USD','XAG','XAU']

for curr in currencies:
    index(curr)
        
df = pd.read_csv('db/index/'+currencies[0]+'.csv')
for i in range(1,len(currencies)):
    df2 = pd.read_csv('db/index/'+currencies[i]+'.csv')
    df = pd.merge(df,df2, on=['date','date'])

df = df.fillna(0)
df = df.set_index('date')


