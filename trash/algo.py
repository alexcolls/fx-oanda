

# import libraries for the module
import json
from oandapyV20 import API
import oandapyV20.endpoints.pricing as pricing
import pandas as pd
pd.options.plotting.backend = "plotly"

#
# YOUR OANDA TOKEN
TOKEN = "37d11dc6e01ec900277bcf70ed296912-60827d532c22d5b1b0d3583a0e9309ef"
# YOUR ACCOUNT ID
ACCOUNT = "101-004-17169350-002"
# SYMBOLS
SYMBOLS = ['XAU_USD']  # 45 fx pairs


api = API(access_token=TOKEN)
r = pricing.PricingStream(accountID=ACCOUNT, params={"instruments": SYMBOLS})
r = api.request(r)


for ticks in r:
    #print(json.dumps(ticks, indent=4), ",")
    if ticks['']
    ask = ticks['closeoutAsk']
    bid = ticks['closeoutBid']
    print(ask, bid)

r.terminate()
r[2]
