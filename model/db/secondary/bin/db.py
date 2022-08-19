
import pandas as pd
pd.options.plotting.backend = "plotly"


def getRawYear ( year, quote='asks'):

    asks = pd.DataFrame()

    for wk in range(1, 10):
        df = pd.read_csv(f'../../primary/data/{str(year)}/{str(wk)}/{quote}.csv', index_col=0)
        df.index = pd.to_datetime(df.index)

        if wk == 1:
            asks = df
        else:
            asks = pd.concat([asks, df], axis=0)
    
    return asks


class prepDataset:

    def __init__ ( self, timeframe='H1' ):

        self.timeframe = timeframe


    def getRawYear ( year, quote='asks'):

        asks = pd.DataFrame()

        for wk in range(1, 52):
            df = pd.read_csv(f'../../primary/data/{str(year)}/{str(wk)}/{quote}.csv', index_col=0)
            df.index = pd.to_datetime(df.index)

            if wk == 1:
                asks = df
            else:
                asks = pd.concat([asks, df], axis=0)
        
        return asks

    def makeReturns ( self ):

        asks = self.getRawYear( 2005, quote='asks')
        bids = self.getRawYear( 2005, quote='bids')

        mids = (asks+bids)/2

        mids['month'] = mids.index.month
        mids['day'] = mids.index.day
        mids['weekday'] = mids.index.weekday
        mids['hour'] = mids.index.hour
        mids['minute'] = mids.index.minute
        mids['second'] = mids.index.second

        mids.reset_index(inplace=True)
        mids.groupby(['month', 'day', 'hour'], as_index=False).mean()
        mids.groupby(['month', 'day', 'hour']).last()


import numpy as np
    
def getWeek( week=2, year=2018, symbol='EUR_CHF' ):
    path = '../../primary/data/'+str(year)+'/'+str(week)+'/'
    df = pd.read_csv(path+'mids.csv', index_col=0)
    ccys = pd.read_csv(path+'ccys.csv', index_col=0)
    sym = pd.DataFrame(df['EUR_GBP'])
    sym['syn'] = ( ccys['EUR'] / ccys['CHF'] )

    sym = pd.DataFrame(ccys)
    fig = idxs.plot()
    fig.show()
    
    idxs = ( np.log(ccys) - np.log(ccys.iloc[0]) )*100
    idxs['jpy'] = ( log(ccys['JPY'] / ccys['JPY'].iloc[0] -1 )*100

    idxs['mean'] = idxs.T.mean()

    fig.show()
    







