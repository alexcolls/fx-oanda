
from cProfile import label
from re import I
from tkinter import Y
from turtle import Shape, title
import pandas as pd
pd.options.plotting.backend = "plotly"


SYMBOLS = [ 'AUD_CAD', 'AUD_CHF', 'AUD_JPY', 'AUD_NZD', 'AUD_USD', 
            'CAD_CHF', 'CAD_JPY', 'CHF_JPY', 'EUR_AUD', 'EUR_CAD', 
            'EUR_CHF', 'EUR_GBP', 'EUR_JPY', 'EUR_NZD', 'EUR_USD', 
            'GBP_AUD', 'GBP_CAD', 'GBP_CHF', 'GBP_JPY', 'GBP_NZD', 
            'GBP_USD', 'NZD_CAD', 'NZD_CHF', 'NZD_JPY', 'NZD_USD', 
            'USD_CAD', 'USD_CHF', 'USD_JPY' ]

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

"""
import numpy as np
    
def getWeek( week=2, year=2008, symbol='EUR_CHF' ):
    path = '../../primary/data/'+str(year)+'/'+str(week)+'/'
    df = pd.read_csv(path+'mids.csv', index_col=0)
    ccys2 = pd.read_csv(path+'ccys.csv', index_col=0)
    sym = pd.DataFrame(df['EUR_GBP'])
    sym['syn'] = ( ccys['EUR'] / ccys['CHF'] )

    sym = pd.DataFrame(ccys)
    fig = idxs.plot()
    fig.show()
    
    idxs = ( np.log(ccys) - np.log(ccys.iloc[0]) )*100
    idxs['jpy'] = ( log(ccys['JPY'] / ccys['JPY'].iloc[0] -1 )*100

    idxs['mean'] = idxs.T.mean()

    fig.show()

def makeCcys2( year, week ):
    path = '../data/' + str(year) +'/'+ str(week)
    mids = pd.read_csv(path+'mids.csv', index_col=0)
    idxs = pd.DataFrame(index=mids.index, columns=ccys)
    for ccy in ccys:
        base = mids[mids.filter(regex=ccy+'_').columns].apply( lambda x: 1/x ).sum(axis=1)
        term = mids[mids.filter(regex='_'+ccy).columns].sum(axis=1)
        idxs[ccy] = round( 1/ (( base + term + 1 ) / (len(ccys)+1)), 10)
    idxs.to_csv( path+'/ccys.csv', index=True )
    del mids, idxs


## create mids.csv & spreads.csv
    def makeMidsSpreads ( self, year, week ):
        # database path
        path = self.db_path +'/'+ str(year) +'/'+ str(week)
        # loads data/asks_bids
        asks = pd.read_csv( path + '/asks.csv', index_col=0 )
        bids = pd.read_csv( path + '/bids.csv', index_col=0 )
        # calculate mid prices
        mids = round((asks+bids)/2, 5)
        # calculate spreads prices
        spreads = round(((asks/bids)-1)*10000, 2)
        # create mids.csv file
        mids.to_csv( path + '/mids.csv' )
        # create spreads.csv file
        spreads.to_csv( path + '/spreads.csv' )
        # log file confirmation
        print('.done')

        # realese memory
        del asks, bids, mids, spreads

    


    ## get currencies (ccys) from symbols (pairs)
    def getCcys ( self ):
        ccys = []
        for sym in self.symbols:
            ccy = sym.split('_')
            if ccy[0] not in ccys:
                ccys.append(ccy[0])
            if ccy[1] not in ccys:
                ccys.append(ccy[1])
        ccys.sort()
        return ccys


    ## create currency basket prices -> ccys.csv
    def makeCcys( self, year, week ):
        path = '../data/' + str(year) +'/'+ str(week)
        mids = pd.read_csv( path+'/mids.csv', index_col=0 )
        idxs = pd.DataFrame(index=mids.index, columns=self.ccys)
        for ccy in self.ccys:
            base = mids[mids.filter(regex=ccy+'_').columns].sum(axis=1)
            term = mids[mids.filter(regex='_'+ccy).columns].apply( lambda x: 1/x ).sum(axis=1)
            idxs[ccy] = round(( base + term + 1 ) / (len(self.ccys)+1), 5)
        idxs.to_csv( path+'/ccys.csv', index=True )
        del mids, idxs
    

"""

ccys = ['AUD', 'CAD', 'CHF', 'EUR', 'GBP', 'JPY', 'NZD', 'USD', 'XAG', 'XAU']


import numpy as np
import pandas as pd

def plotWeek( year=2020, week=1 ):

    path = '../../primary/data/'+str(year)+'/'+str(week)+'/'

    # load mid prices
    mids = pd.read_csv(path+'mids.csv', index_col=0)
    asks = pd.read_csv(path+'asks.csv', index_col=0)
    bids = pd.read_csv(path+'bids.csv', index_col=0)

    # create portfolio returns
    mids_ = ( np.log(mids) - np.log(mids.iloc[0]) )*100

    # plot portfolio returns
    mids_.plot(title=f'Weekly market returns (%) {year}, week {week}').show()

    # load spreads
    spreads = pd.read_csv(path+'spreads.csv', index_col=0)
    spreads.plot(title='Spreads (%%)').show()

    # create currency indexes 
    idxs = pd.DataFrame(index=mids.index, columns=ccys)
    idxs_asks = pd.DataFrame(index=asks.index, columns=ccys)
    idxs_bids = pd.DataFrame(index=asks.index, columns=ccys)
    for ccy in ccys:
        #base = mids[mids.filter(regex=ccy+'_').columns].apply( lambda x: 1/x ).sum(axis=1)
        #term = mids[mids.filter(regex='_'+ccy).columns].sum(axis=1)
        #idxs[ccy] = round( 1/ (( base + term + 1 ) / (len(ccys)+1)), 10)

        x_asks = asks[asks.filter(regex=ccy+'_').columns].apply( lambda x: 1/x ).sum(axis=1)
        y_asks = bids[bids.filter(regex='_'+ccy).columns].sum(axis=1)
        idxs_asks[ccy] = 1/ (( x_asks + y_asks + 1 ) / len(ccys))

        x_bids = bids[bids.filter(regex=ccy+'_').columns].apply( lambda x: 1/x ).sum(axis=1)
        y_bids = asks[asks.filter(regex='_'+ccy).columns].sum(axis=1)
        idxs_bids[ccy] = 1/ (( x_bids + y_bids + 1 ) / len(ccys))

    # create currency-idx returns
    idxs_ = ( np.log(idxs) - np.log(idxs.iloc[0]) )*100

    idxs_asks_ = ( np.log(idxs_asks) - np.log(idxs_asks.iloc[0]) )*100
    idxs_bids_ = ( np.log(idxs_bids) - np.log(idxs_bids.iloc[0]) )*100

    idxs__ = pd.merge(idxs_asks_, idxs_bids_, how='inner', left_index=True, right_index=True)

    # plot currency returns
    idxs_.plot(title=f'Currency idx returns % {year}, week {week}').show()

    idxs_asks_.plot(title=f'Currency idx returns % {year}, week {week}').show()

    # create momentum signal
    mom_ = pd.DataFrame(index=idxs.index, columns=ccys)

    for i in range(10, len(idxs_)):
        for ccy in ccys:
            #mom_[ccy][i] = idxs_[ccy][i] - idxs_[ccy][i-1]
            mom_[ccy][i] = ( idxs_asks[ccy][i] - idxs_asks[ccy][i-1] ) - ( idxs_bids[ccy][i] - idxs_bids[ccy][i-1] )

    mom_.plot(title=f'Momentum % {year}, week {week}', markers=True).show()


    asks_ = ( np.log(asks) - np.log(asks.iloc[0]) )*100
    bids_ = ( np.log(bids) - np.log(bids.iloc[0]) )*100


    for ccy in ccys:

        x_asks = asks_[asks_.filter(regex=ccy+'_').columns].sum(axis=1)
        y_asks = bids_[bids_.filter(regex='_'+ccy).columns].sum(axis=1)
        idxs_asks[ccy] = ( x_asks - y_asks ) / len(ccys)

        x_bids = bids_[bids_.filter(regex=ccy+'_').columns].sum(axis=1)
        y_bids = asks_[asks_.filter(regex='_'+ccy).columns].sum(axis=1)
        idxs_bids[ccy] = ( x_bids - y_bids ) / len(ccys)


    idxs_ = pd.merge(idxs_asks, idxs_bids, how='inner', left_index=True, right_index=True)




"""

# create weekly currency Kings & Queens
Ks = pd.DataFrame(index=idxs.index, columns=ccys)
Qs = pd.DataFrame(index=idxs.index, columns=ccys)

for i in range(10, len(idxs_)):
    for ccy in ccys:
        Ks[ccy][i] = idxs_[ccy][i] - min(idxs_[ccy][:i])
        Qs[ccy][i] = idxs_[ccy].iloc[i] - max(idxs_[ccy][:i])

# plot Kings & Queens
Ks.plot(title='Weekly Kings').show()
Qs.plot(title='Weekly Queens').show()


# create weekly currency Kings & Queens
Mean = pd.DataFrame(index=idxs.index, columns=ccys)
StDev = pd.DataFrame(index=idxs.index, columns=ccys)

for i in range(10, len(idxs_)):
    for ccy in ccys:
        Mean[ccy][i] = idxs_[ccy][:i].mean()
        StDev[ccy][i] = idxs_[ccy][:i].std()

Mean.plot(title='Weekly Mean').show()
StDev.plot(title='Weekly StDev').show()

Sharpe = Mean / StDev
Sharpe.plot(title='Sharpe ratio').show()


zsc = pd.DataFrame(index=idxs.index, columns=ccys)

for i in range(len(idxs)):
    for ccy in ccys:
        if idxs[ccy][i] > idxs[ccy][i-1]:
            zsc[ccy][i] = 1
        elif idxs[ccy][i] < idxs[ccy][i-1]:
            zsc[ccy][i] = -1
        else:
            zsc[ccy][i] = 0

zsc = zsc.cumsum()

zsc.plot().show()

idxs2.corr()

idxs2.index = pd.to_datetime(idxs2.index)

corrs = pd.DataFrame(index=idxs2.index, columns=SYMBOLS)

state = True

for i in range(len(idxs2)):
    if state:
        if idxs2.index[i].weekday() == 0 and idxs2.index[i].hour == 12:
            state = False
    else:
        for sym in corrs.columns:
            x = idxs2[sym[:3]][:i]
            y = idxs2[sym[4:]][:i]
            corrs[sym][i] = np.corrcoef(x, y)[0][1]

corrs.plot().show()


idxs2.index[0].hour


"""





