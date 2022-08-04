
import pandas as pd


def getPrices ( year, quote='asks'):

    asks = pd.DataFrame()

    for wk in range(1, 10):
        df = pd.read_csv(f'../../primary/data/{str(year)}/{str(wk)}/{quote}.csv', index_col=0)
        df.index = pd.to_datetime(df.index)

        if wk == 1:
            asks = df
        else:
            asks = pd.concat([asks, df], axis=0)
    
    return asks
    




