
import __key__
import __symbols__

import json
import requests
import pandas as pd
from pathlib import Path

from datetime import datetime
from datetime import timedelta

# OANDA BROKER DATA-FEED API

class OandaApi:

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

    def __init__  ( self, LIVE_TRADING=False,  TOKEN=__key__.TOKEN ):
        
        self.enviroment = self.ENVIRONMENTS['no_trading']['api']
        if LIVE_TRADING:
            self.enviroment = self.ENVIRONMENTS['live']

        self.client = requests.Session()
        self.client.headers['Authorization'] = 'Bearer '+ TOKEN
        # self.prices = self.getPrices()


    def getYearsWeeks (  self, year=2017, symbols=__symbols__.SYMBOLS, api_version='v3' ):

        # get first monday of the year
        first_monday = timedelta( days=( 7 - datetime.strptime(str(year), '%Y').weekday() ) )
        first_monday = datetime.strptime(str(year), '%Y') + first_monday

        # get last friday of the year
        last_friday = timedelta(days=( 3 + datetime.strptime(str(year+1), '%Y').weekday()) )
        last_friday = datetime.strptime(str(year+1), '%Y') - last_friday

        mondays = [ first_monday + timedelta(weeks=i) for i in range(51) ]

        for i, monday in enumerate(mondays):
            if monday.weekday() == 0:
                mondays[i] = datetime.strftime(monday, '%Y-%m-%d') + 'T00:00:00.000000000Z'
            else:
                print('Its not a Monday!', i)

        wk = 0
        
        for monday in mondays:

            wk += 1

            asks = pd.DataFrame()
            bids = pd.DataFrame()

            for symbol in symbols:

                print(symbol, 'week ', wk)

                data = { 'dt': [], 'ask': [], 'bid': [] }

                start_date = monday
                friday = False
                iterate = True

                while iterate:

                    # request 5 second candles from oanda rest-api
                    req = self.client.get(f'{self.enviroment}/{api_version}/instruments/{symbol}/candles?count=5000&price=BA&granularity=S5&from={start_date}&includeFirst=False')
                    req = json.loads(req.content.decode('utf-8'))['candles']

                    print(start_date[:19], req[-1]['time'][:19])

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
                    asks = pd.merge(asks, _asks, how='inner', left_index=True, right_index=True)
                    bids = pd.merge(bids, _bids, how='inner', left_index=True, right_index=True)

                print(asks)

                del data, _asks, _bids

            return asks

            
            
            
        

oanda = OandaApi()


