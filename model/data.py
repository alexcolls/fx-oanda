
import json
import requests
import pandas as pd

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
        self.candles = self.Candles()

    def Candles( self, symbols=__symbols__.SYMBOLS, timeframe='S5', from_date='2022-01-01', version='v3'  ):

        candles = {}

        for symbol in symbols:

            print(symbol)

            asks = { 'dt': [], 'o': [], 'h': [], 'l': [], 'c':[], 'v': [] }
            bids = { 'dt': [], 'o': [], 'h': [], 'l': [], 'c':[], 'v': [] }

            start_date = from_date

            while True:

                req = self.client.get(f'https://api-fxpractice.oanda.com/{version}/instruments/{symbol}/candles?count=5000&price=BA&granularity={timeframe}&from={start_date}')
            
                req = json.loads(req.content.decode('utf-8'))['candles']

                for x in req:
                    asks['dt'].append(x['time'])
                    asks['o'].append(float(x['ask']['o']))
                    asks['h'].append(float(x['ask']['h']))
                    asks['l'].append(float(x['ask']['l']))
                    asks['c'].append(float(x['ask']['c']))
                    asks['v'].append(float(x['ask']['c']))

                    bids['dt'].append(x['time'])
                    bids['o'].append(float(x['bid']['o']))
                    bids['h'].append(float(x['bid']['h']))
                    bids['l'].append(float(x['bid']['l']))
                    bids['c'].append(float(x['bid']['c']))
                    bids['v'].append(float(x['bid']['c']))
        
                if start_date == asks['dt'][-1]:
                    del req
                    break

                start_date = asks['dt'][-1]
    
            asks = pd.DataFrame.from_dict(asks)
            asks.dt = pd.to_datetime(asks.dt)
            asks = asks.set_index('dt')
            bids = pd.DataFrame.from_dict(bids)
            bids.dt = pd.to_datetime(bids.dt)
            bids = bids.set_index('dt')

            candles[symbol] = { 'asks': asks, 'bids': bids }
            
            del asks, bids
        
        self.candles = candles

        del candles

        return self.candles


oanda = OandaApi()
