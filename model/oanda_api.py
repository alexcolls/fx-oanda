
import __key__
import __symbols__

import json
import requests
import pandas as pd
from pathlib import Path

# OANDA BROKER DATA-FEED API

class OandaApi:

    ENVIRONMENTS = {
        "no_trading": {
            "stream": 'https://stream-fxpractice.oanda.com',
            "api": 'https://api-fxpractice.oanda.com'
        },
        "live": {
            "stream": 'https://stream-fxtrade.oanda.com',
            "api": 'https://api-fxtrade.oanda.com'
        }
    }

    def __init__  ( self, LIVE_TRADING=False,  TOKEN=__key__.TOKEN ):
        
        self.enviroment = self.ENVIRONMENTS['no_trading']['api']
        if LIVE_TRADING:
            self.enviroment = self.ENVIRONMENTS['live']

        self.client = requests.Session()
        self.client.headers['Authorization'] = 'Bearer '+ TOKEN
        # self.prices = self.Prices()


    def Prices( self, symbols=__symbols__.SYMBOLS, timeframe='S5', from_year=2022, to_year=2022, version='v3' ):

        for yr in range(int(from_year), int(to_year)+1):
            
            for symbol in symbols:

                print(symbol)

                data = { 'dt': [], 'ask': [], 'bid': [], 'vol': [] }

                start_date = str(yr)+'-01-01'

                iterate = True

                while iterate:

                    req = self.client.get(f'{self.enviroment}/{version}/instruments/{symbol}/candles?count=5000&price=BA&granularity={timeframe}&from={start_date}')

                    req = json.loads(req.content.decode('utf-8'))['candles']

                    digits = len(req[0]['ask']['c'].split('.')[1])
                    year = req[0]['time'][:4]

                    for x in req:
                        year = x['time'][:4]
                        if year != str(yr):
                            iterate = False
                            break

                        data['dt'].append(x['time'])
                        data['vol'].append(int(x['volume']))
                        for p in ['ask', 'bid']:
                            o = float(x[p]['o'])
                            h = float(x[p]['h'])
                            l = float(x[p]['l'])
                            c = float(x[p]['c'])
                            data[p].append( round((o+h+l+c*2)/5, digits) )
                        
                    if start_date == data['dt'][-1]:
                        del req
                        break

                    start_date = data['dt'][-1]
        
                data = pd.DataFrame.from_dict(data)
                data.dt = pd.to_datetime(data.dt)
                data = data.set_index('dt')
                data = data[~data.index.duplicated(keep='first')]        
                
                path = 'db/prices/'+str(yr)
                Path(path).mkdir(parents=True, exist_ok=True)
                data.to_csv(path+symbol+'.csv', index=True)

                del data



oanda = OandaApi()
