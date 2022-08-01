
import json
import requests
import pandas as pd

import oandapyV20.endpoints.forexlabs as labs

import __key__
import __symbols__


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


    def Prices( self, symbols=__symbols__.SYMBOLS, timeframe='S5', from_date='2022-01-01', version='v3' ):

        for symbol in symbols:

            print(symbol)

            data = { 'dt': [], 'ask': [], 'bid': [], 'vol': [] }

            start_date = from_date

            while True:

                req = self.client.get(f'{self.enviroment}/{version}/instruments/{symbol}/candles?count=5000&price=BA&granularity={timeframe}&from={start_date}')
            
                req = json.loads(req.content.decode('utf-8'))['candles']

                for x in req:
                    data['dt'].append(x['time'])
                    data['vol'].append(int(x['volume']))
                    for p in ['ask', 'bid']:
                        o = float(x[p]['o'])
                        h = float(x[p]['h'])
                        l = float(x[p]['l'])
                        c = float(x[p]['c'])
                        data[p].append((o+h+l+c*2)/5)
                    
                if start_date == data['dt'][-1]:
                    del req
                    break

                start_date = data['dt'][-1]
    
            data = pd.DataFrame.from_dict(data)
            data.dt = pd.to_datetime(data.dt)
            data = data.set_index('dt')
            data = data[~data.index.duplicated(keep='first')]        
            
            self.prices[symbol] = data

            del data

        return self.prices


    def CoT ( self, symbol='EUR_USD', version='v3' ):
        
        req = self.client.get(f'{self.enviroment}/labs/{version}/commitments_of_traders?instrument={symbol}')
        
        req = json.loads(req.content.decode('utf-8'))[symbol]

        data = { 'dt': [], 'price': [], 'bid': [], 'vol': [] }

        for x in req:
            data['dt'].append(pd.to_datetime(x['date']))


        return req


oanda = OandaApi()
