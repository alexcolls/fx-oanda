from os import listdir
import pandas as pd

def index( currency ):
    print(currency+'...')
    files = [k for k in listdir('db') if currency in k]
    df = pd.read_csv('db/'+files[0])
    if files[0][0:3] != currency: df['return'] = -df['return']
    df = df.rename(columns={'return':files[0][0:7]})
    for i in range(len(files)-1):
        df2 = pd.read_csv('db/'+files[i+1])
        if files[i+1][0:3] != currency: df2['return'] = -df2['return']
        df2 = df2.rename(columns={'return':files[i+1][0:7]})
        df = pd.merge(df,df2, on=['date','date'])
    df = df.fillna(0)
    df = df.set_index('date')
    df[currency] = round(df.sum(axis=1),2)
    df = df[currency]
    df.to_csv('db/index/'+currency+'.csv', index=True)


currencies = ['AUD','CAD','CHF','EUR','GBP','HKD','JPY','NZD','SGD','USD','XAG','XAU']

for curr in currencies:
    index(curr)
        

for file in currencies:


