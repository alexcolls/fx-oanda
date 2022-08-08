
# OANDA BROKER REST API

# author: Quantium Rock
# date: August 2022
# license: MIT

# config files
from apis.__auth__ import TOKEN

# dependencies
import requests
import json

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

    def __init__  ( self, LIVE_TRADING=False,  TOKEN=TOKEN ):
        
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


    # ORDER EXECUTOR

        # TODO


# END