
# OANDA BROKER REST API

# author: Quantium Rock
# date: August 2022
# license: MIT

# config files
import __auth__
import __universe__

# dependencies
import requests
import json
from pathlib import Path
from datetime import datetime
from datetime import timedelta
import pandas as pd

# API CLIENT

class OandaApi:

    # url constants
    ENVIRONMENTS = {
        # demo account
        "no_trading": {
            "stream": 'https://stream-fxpractice.oanda.com',
            "api": 'https://api-fxpractice.oanda.com'
        },
        # real account
        "live": {
            "stream": 'hstart_datettps://stream-fxtrade.oanda.com',
            "api": 'https://api-fxtrade.oanda.com'
        }
    }

    def __init__  ( self, LIVE_TRADING=False,  TOKEN=__auth__.TOKEN ):
        
        # set trading enviroment
        self.enviroment = self.ENVIRONMENTS['no_trading']['api']
        if LIVE_TRADING:
            self.enviroment = self.ENVIRONMENTS['live']

        # set request session  and add authentification metadata
        self.client = requests.Session()
        self.client.headers['Authorization'] = 'Bearer '+ TOKEN


    #__ OandaApi.getRawCandles('EUR_USD', 'H1', '2022-01-01')

    def getRawCandles ( self, symbol, timeframe, start_date, count=5000, include_frist=False, api_version='v3' ):

        req = self.client.get(f'{self.enviroment}/{api_version}/instruments/{symbol}/candles?count={count}&price=BA&granularity={timeframe}&from={start_date}&includeFirst={include_frist}')

        return json.loads(req.content.decode('utf-8'))['candles']


    #__ OandaApi.getWeeksOfYear(2022)
        """ 
            ,input = year
            ,download candles (bid/ask), min granularity = 5 seconds
            ,for each symbol in the portfolio, by default __universe__.SYMBOLS
            ,from the first monday to the last friday[-2] of the year
            ,group all symbols data by weeks
            ,store each week locally into ../data/
         """
    def storeYearlyQuotes (  self, year=2022, start_week=1, timeframe='S5', symbols=__universe__.SYMBOLS,  ):

        # get first monday of the year
        first_monday = timedelta( days=( 7 - datetime.strptime(str(year), '%Y').weekday() ))
        first_monday = datetime.strptime(str(year), '%Y') + first_monday

        # get all mondays of the year, except last one
        mondays = [ first_monday + timedelta(weeks=i) for i in range(start_week-1, 51) ]

        # check mondays dates and add utc timezone
        for i, monday in enumerate(mondays):
            if monday.weekday() == 0:
                mondays[i] = datetime.strftime(monday, '%Y-%m-%d') + 'T00:00:00.000000000Z'
            else:
                print('Its not a Monday!', i)

        wk = 0 # init weeks counter
        
        # iterate on each monday of the year (weeks)
        for monday in mondays:

            wk += 1 # sum 1 week

            # get each datetime of the week by timeframe ( default=5seconds )
            day_timestamps = pd.date_range(pd.to_datetime(monday), pd.to_datetime(monday)+timedelta(days=5), freq=timeframe[::-1])[:-1]

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

                    # request 5 second candles from oanda rest-api
                    req = self.getRawCandles( symbol, timeframe, start_date )

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

                # realise memory
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

            # realise memory
            del asks, bids

        # ^ finished all weeks


    # ORDER EXECUTOR

        # TODO
            


# end
