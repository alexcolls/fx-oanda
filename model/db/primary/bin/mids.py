
# author: Quantium Rock
# license: MIT

import os
import pandas as pd

db_path = '../data/asks_bids'

# iterate data/asks_bids db to apply <function>
def _iterateDB ( function ):
    # function wrapper
    def wrapper():
        # iterate years directories
        for yr in os.scandir(db_path):
            # check if it's a directory
            if yr.is_dir():
                # iterate weeks directories
                for wk in os.scandir(yr.path):
                    # check if it's a directory
                    if wk.is_dir():
                        # exec function
                        function(wk.path)
                        # print(wk.path)
    return  wrapper

# iterating data/asks_bids db to apply <makeMids>
@_iterateDB
# create mid=(a+b)/2 prices db
def makeMids ( path ):
    # loads data/asks_bids
    asks = pd.read_csv( path + '/asks.csv', index_col=0 )
    bids = pd.read_csv( path + '/bids.csv', index_col=0 )
    # calculate mid prices
    mids = round((asks+bids)/2, 5)
    # create mids.csv file
    mids.to_csv( path.replace('asks_bids', 'mids') + '/mids.csv' )
    # log file confirmation
    print(path, 'done')

# delete all data/mids #dontaskwhy
def deleteMids( path ):
    for yr in os.scandir('../data/mids'):
        if yr.is_dir():
            for wk in os.scandir(yr.path):
                if wk.is_dir():
                    for file in os.scandir(wk.path):
                        if 'mids.csv' == str(file).split("'")[1]:
                            os.remove(file)

