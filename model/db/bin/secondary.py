
import numpy as np
import pandas as pd


class SecondaryData:

    def __init__ ( self ):
        pass

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

    def makeData( year=2020, week=1 ):

        in_path = '../../primary/data/'+str(year)+'/'+str(week)+'/'

        # load mid prices
        mids = pd.read_csv(in_path+'mids.csv', index_col=0)

        # create portfolio returns (standarize protfolio prices %)
        mids_ = ( np.log(mids) - np.log(mids.iloc[0]) )*100

        out_path = '../../secondary/data/'+str(year)+'/'+str(week)+'/'




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

