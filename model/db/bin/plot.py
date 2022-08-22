
import numpy as np
import pandas as pd
pd.options.plotting.backend = "plotly"

def plotPrimaryData( year=2022, week=1 ):

    path = 'db/data/primary/'+str(year)+'/'+str(week)+'/'

    # load mid prices
    mids = pd.read_csv(path+'mids.csv', index_col=0)

    # create portfolio returns
    mids_ = ( np.log(mids) - np.log(mids.iloc[0]) )*100

    # plot portfolio returns
    mids_.plot(title=f'Weekly market returns (%) {year}, week {week}').show()