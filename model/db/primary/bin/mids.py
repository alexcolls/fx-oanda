
# author: Quantium Rock
# license: MIT

import os
import pandas as pd
from pathlib import Path

db_path = '../data/asks_bids'


# iterate data/asks_bids db to apply <function>
def _iterateAsksBids ( function ):
    # function wrapper
    def wrapper():
        # iterate years directories
        for yr in os.scandir(db_path):
            # check if year is a directory
            if yr.is_dir():
                # iterate weeks directories
                for wk in os.scandir(yr.path):
                    # check if week is a directory
                    if wk.is_dir():
                        # exec function
                        function(wk.path, str(yr).split("'")[1], str(wk).split("'")[1])
                        # print(wk.path)
    return  wrapper


# iterating data/asks_bids db to apply <makeMids>
@_iterateAsksBids
# create mid=(a+b)/2 prices db
def makeMids ( path, year, week ):
    # loads data/asks_bids
    asks = pd.read_csv( path + '/asks.csv', index_col=0 )
    bids = pd.read_csv( path + '/bids.csv', index_col=0 )
    # calculate mid prices
    mids = round((asks+bids)/2, 5)
    # create path ../data/<year>/<week>/
    path_mids = '../data/mids/'+str(year)+'/'+str(week)+'/'
    print('...saving', path_mids)
    Path(path_mids).mkdir(parents=True, exist_ok=True)
    # create mids.csv file
    mids.to_csv( path_mids + '/mids.csv' )
    # log file confirmation
    print(path, 'done')

    # realese memory
    del asks, bids, mids

# delete all data/<year>/<week>/mids.csv -dontaskwhy
def deleteMids( path ):
    for yr in os.scandir('../data/mids'):
        if yr.is_dir():
            for wk in os.scandir(yr.path):
                if wk.is_dir():
                    for file in os.scandir(wk.path):
                        # 
                        if 'mids.csv' == str(file).split("'")[1]:
                            os.remove(file)

# END