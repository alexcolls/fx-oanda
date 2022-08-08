
# author: Quantium Rock
# license: MIT

import os
from pathlib import Path
from datetime import datetime
from datetime import timedelta
import pandas as pd

from apis.oanda_api import OandaApi
from __universe__ import SYMBOLS


class PrimaryData:

    def __init__ ( self, timeframe='S5' ):
        self.timeframe = timeframe
        self.db_path = '../data/'


    def checkDB ( self, start_year=2005 ):

        missing_years = []
        current_year = datetime.utcnow().year
        years = [ yr for yr in range(start_year, current_year+1) ]

        missing_weeks = {}
        current_week = datetime.strptime(str(current_year)+'-01-01', '%Y-%m-%d')
        current_week = ( datetime.utcnow() - current_week ) / timedelta(weeks=1)
        current_week = int(current_week)

        years_db = os.listdir(self.db_path)
        for year in years:
            if not str(year) in years_db:
                print('Missing year:', year)
                missing_years.append(year)
            else:
                weeks_db = os.listdir(self.db_path + str(year))
                wks = current_week if year == current_year else 52
                missing_weeks[year] = []
                for week in range(1, wks):
                    if not str(week) in weeks_db:
                        print('Missing week:', week, 'from', year)
                        missing_weeks[year].append(week)

        # delete empty keys
        missing_weeks = dict( [ (k,v) for k, v in missing_weeks.items() if len(v) > 0 ] )

        if len(missing_weeks) == 0 and len(missing_years) == 0:
            print('Nice! Primary DB is full!')

        return missing_years, missing_weeks
    

    def updateDB ( self ):

        missing_years, missing_weeks = self.checkDB()

        for year in missing_years:
            print('\nDownloading year...', year)
            self.getQuotesOfYear( year )
        
        for year, weeks in missing_weeks.items():
            for week in weeks:
                print('\nDownloading week...', week, year)
                self.getQuotesOfYear( year=year, start_week=week, end_week=week )

        print('Primary DB updated!')
        
        return True


    #__ primaryDB.getQuotesOfYear(2022)
        """ 
            1. download candles (bid/ask), min granularity = 5 seconds
            2. for each symbol in the portfolio, by default __universe__.SYMBOLS
            3. from the first monday to the last friday[-2] of the year
            4. group all symbols data by weeks
            5. store each week locally into ../data/
         """
    def getQuotesOfYear (  self, year=2022, start_week=1, end_week=51, symbols=SYMBOLS ):

        oanda_api = OandaApi()

        # get first monday of the year
        first_monday = timedelta(days=( 7 - datetime.strptime(str(year), '%Y').weekday()))
        first_monday = datetime.strptime(str(year), '%Y') + first_monday

        # get all mondays of the year, except last one
        mondays = [ first_monday + timedelta(weeks=i) for i in range(start_week-1, end_week) ]

        # check mondays dates and add utc timezone
        for i, monday in enumerate(mondays):
            if monday.weekday() == 0:
                mondays[i] = datetime.strftime(monday, '%Y-%m-%d') + 'T00:00:00.000000000Z'
            else:
                print('Its not a Monday!', i)

        wk = start_week-1 # init weeks counter
        
        # iterate on each monday of the year (weeks)
        for monday in mondays:

            wk += 1 # sum 1 week

            # get each datetime of the week by timeframe ( default=5seconds )
            day_timestamps = pd.date_range(pd.to_datetime(monday), pd.to_datetime(monday) + timedelta(days=5), freq=self.timeframe[::-1])[:-1]

            # init daily dataframes indices for asks & bids
            asks = pd.DataFrame(index=day_timestamps)
            bids = pd.DataFrame(index=day_timestamps)

            # iterate each __universe__.SYMBOL to get a full week data each
            for symbol in symbols:

                # print symbol and week of the year
                print(symbol, 'week', wk)

                # initialize symbol variable
                data = { 'dt': [], 'ask': [], 'bid': [] }
                start_date = monday
                iterate = True

                # iterate until the end of week
                while iterate:

                    # request 5000 5-second-bars from oanda rest-api
                    req = oanda_api.getRawCandles( symbol, self.timeframe, start_date )

                    # print first date and last date of the request
                    print(req[0]['time'][:19], req[-1]['time'][:19])

                    # get the number of decimals of instrument's price
                    digits = len(req[0]['ask']['c'].split('.')[1])

                    # iterate each candle
                    for x in req:
                        
                        # if current candle time changed week
                        if pd.to_datetime(x['time']) > asks.index[-1]:
                            iterate = False
                            break # close week

                        # append to data bid/ask quotes
                        data['dt'].append(x['time'])
                        for p in ['ask', 'bid']:
                            o = float(x[p]['o'])
                            h = float(x[p]['h'])
                            l = float(x[p]['l'])
                            c = float(x[p]['c'])
                            data[p].append( round((o+h+l+c*2)/5, digits) )
                    
                    if len(data['dt']) > 0:
                    # only for current year: check if there is no more history
                        if start_date == data['dt'][-1]:
                            iterate = False
                            del req
                            break
                        # otherwise update start_date with last loop request
                        start_date = data['dt'][-1]

                # ^ finished symbol week

                # transform data to asks dataframe
                _asks = pd.DataFrame(data['ask'], index=data['dt'], columns=[symbol])
                _asks.index = pd.to_datetime(_asks.index)
                
                # transform data to bids dataframe
                _bids = pd.DataFrame(data['bid'], index=data['dt'], columns=[symbol])
                _bids.index = pd.to_datetime(_bids.index)

                # symbol dataframe to the daily portfolio
                asks = pd.merge(asks, _asks, how='outer', left_index=True, right_index=True)
                bids = pd.merge(bids, _bids, how='outer', left_index=True, right_index=True)

                # realese memory
                del data, _asks, _bids

            # ^ finished all symbols

            # fill nans with forward-fill (last non-nan price)
            asks.fillna(method='ffill', inplace=True)
            bids.fillna(method='ffill', inplace=True)

            # fill nans with backward-fill (for the first seconds of the week)
            asks.fillna(method='bfill', inplace=True)
            bids.fillna(method='bfill', inplace=True)

            # create path ../data/<year>/<week>/
            path = '../data/'+str(year)+'/'+str(wk)+'/'
            print('...saving', path)
            Path(path).mkdir(parents=True, exist_ok=True)

            # save daily csv into year week folder
            asks.to_csv(path+'asks.csv', index=True)
            bids.to_csv(path+'bids.csv', index=True)

            # realese memory
            del asks, bids

        # ^ finished all weeks

    #_


    def _iterateDB ( self, function ):
        def wrapper():
            for yr in os.scandir(self.db_path):
                if yr.is_dir():
                    for wk in os.scandir(yr.path):
                        if wk.is_dir():
                            function(wk.path)
                            # print(wk.path)
        return wrapper


    @_iterateDB
    def makeMids ( self, path=None ):
        asks = pd.read_csv( path + '/asks.csv', index_col=0 )
        bids = pd.read_csv( path + '/bids.csv', index_col=0 )
        mids = round( (asks+bids)/2, 5)
        mids.to_csv( path + '/mids.csv' )
        print(path, 'done')

    """
    @_iterateDB
    def makeIndices( path ):
        mids = pd.read_csv( path + '/mids.csv', index_col=0 )
    """

    
