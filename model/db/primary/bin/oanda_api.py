
# OANDA BROKER REST API

# config files
import __auth__
import __symbols__

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
        "no_trading": {
            "stream": 'https://stream-fxpractice.oanda.com',
            "api": 'https://api-fxpractice.oanda.com'
        },
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

    #__ OandaApi.getWeeksOfYear(2022)
        """ 
            ,input = year
            ,download candles (bid/ask), min granularity = 5 seconds
            ,for each symbol in the portfolio, by default __symbols__.SYMBOLS
            ,from the first monday to the last friday[-2] of the year
            ,group all symbols data by weeks
            ,store each week locally
         """
    def getWeeksOfYear (  self, year, symbols=__symbols__.SYMBOLS, api_version='v3' ):

        """       
            # get last friday of the year
            last_friday = timedelta( days=( 3 + datetime.strptime(str(year+1), '%Y').weekday() ))
            last_friday = datetime.strptime(str(year+1), '%Y') - last_friday
        """

        # get first monday of the year
        first_monday = timedelta( days=( 7 - datetime.strptime(str(year), '%Y').weekday() ))
        first_monday = datetime.strptime(str(year), '%Y') + first_monday

        # get all mondays of the year
        mondays = [ first_monday + timedelta(weeks=i) for i in range(51) ]

        # check mondays dates and add utc timezone
        for i, monday in enumerate(mondays):
            if monday.weekday() == 0:
                mondays[i] = datetime.strftime(monday, '%Y-%m-%d') + 'T00:00:00.000000000Z'
            else:
                print('Its not a Monday!', i)

        wk = 0 # init weeks counter
        
        # iterate on each monday of the year (weeks)
        for monday in mondays:

            wk += 1
            # init weekly dataframes
            asks = pd.DataFrame()
            bids = pd.DataFrame()

            # iterate each __symbols__.SYMBOL to get a full week data each
            for symbol in symbols:

                # 
                print(symbol, 'week ', wk)

                data = { 'dt': [], 'ask': [], 'bid': [] }

                start_date = monday
                friday = False
                iterate = True

                while iterate:

                    # request 5 second candles from oanda rest-api
                    req = self.client.get(f'{self.enviroment}/{api_version}/instruments/{symbol}/candles?count=5000&price=BA&granularity=S5&from={start_date}&includeFirst=False')
                    req = json.loads(req.content.decode('utf-8'))['candles']

                    print(req[0]['time'][:19], req[-1]['time'][:19])

                    if not friday and datetime.strptime(req[0]['time'][:19], '%Y-%m-%dT%H:%M:%S').weekday() == 4:
                        friday = True

                    digits = len(req[0]['ask']['c'].split('.')[1])

                    for x in req:
                        
                        if friday and datetime.strptime(x['time'][:19], '%Y-%m-%dT%H:%M:%S').weekday() != 4:
                            iterate = False
                            break

                        data['dt'].append(x['time'])
                        for p in ['ask', 'bid']:
                            o = float(x[p]['o'])
                            h = float(x[p]['h'])
                            l = float(x[p]['l'])
                            c = float(x[p]['c'])
                            data[p].append( round((o+h+l+c*2)/5, digits) )
                        
                    if start_date == data['dt'][-1]:
                        iterate = False
                        del req
                        break

                    start_date = data['dt'][-1]

                _asks = pd.DataFrame(data['ask'], index=data['dt'], columns=[symbol])
                _asks.index = pd.to_datetime(_asks.index)
                _bids = pd.DataFrame(data['bid'], index=data['dt'], columns=[symbol])
                _bids.index = pd.to_datetime(_bids.index)

                if len(asks) == 0:
                    asks = _asks
                    bids = _bids
                else:
                    asks = pd.merge(asks, _asks, how='outer', left_index=True, right_index=True)
                    bids = pd.merge(bids, _bids, how='outer', left_index=True, right_index=True)

                print(asks)

                del data, _asks, _bids

            asks = asks.fillna(method='ffill')[1:]
            bids = bids.fillna(method='ffill')[1:]

            

            del asks, bids
            


    # ORDER EXECUTOR

        # TODO
            
            
        

oanda = OandaApi()


