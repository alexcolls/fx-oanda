
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


    





