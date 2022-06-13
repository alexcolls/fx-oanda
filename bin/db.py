# script


from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
from datetime import timedelta, date, datetime
from pathlib import Path
from numpy import isnan
import pandas as pd
import sys

import key

client = API(access_token=key.token)

symbols = ['AUD_CAD', 'AUD_CHF', 'AUD_HKD', 'AUD_JPY', 'AUD_NZD', 'AUD_SGD', 'AUD_USD',
           'CAD_CHF', 'CAD_HKD', 'CAD_JPY', 'CAD_SGD', 'CHF_HKD', 'CHF_JPY', 'EUR_AUD',
           'EUR_CAD', 'EUR_CHF', 'EUR_GBP', 'EUR_HKD', 'EUR_JPY', 'EUR_NZD', 'EUR_SGD',
           'EUR_USD', 'GBP_AUD', 'GBP_CAD', 'GBP_CHF', 'GBP_HKD', 'GBP_JPY', 'GBP_NZD',
           'GBP_SGD', 'GBP_USD', 'HKD_JPY', 'NZD_CAD', 'NZD_CHF', 'NZD_HKD', 'NZD_JPY',
           'NZD_SGD', 'NZD_USD', 'SGD_CHF', 'SGD_HKD', 'SGD_JPY', 'USD_CAD', 'USD_CHF',
           'USD_HKD', 'USD_JPY', 'USD_SGD']  # 45 fx pairs


def importdb(year, symbols):

    # prepare dataframe
    def prepdf(year):

        def daterange(date1, date2):
            for n in range(int((date2 - date1).days)+1):
                yield date1 + timedelta(n)

        start_dt = date(year, 1, 1)
        end_dt = date(year, 12, 31)

        dates = []
        weekdays = [5, 6]
        for dt in daterange(start_dt, end_dt):
            if dt.weekday() not in weekdays:
                dates.append(dt.strftime("%Y-%m-%d"))

        return pd.DataFrame(index=dates, columns=symbols)

    y = year
    more = True
    while more:

        prices = prepdf(y)
        changs = prepdf(y)
        volats = prepdf(y)

        _from = str(y)+'-01-01'
        _to = str(y)+'-12-31'
        # if it's current year
        if y == datetime.today().year:
            _to = str(datetime.today())[0:10]
            prices = prices.truncate(after=_to)
            changs = changs.truncate(after=_to)
            volats = volats.truncate(after=_to)
            more = False

        params = {'granularity': 'D', 'from': _from, 'to': _to}

        # import from oanda
        for sym in symbols:
            r = instruments.InstrumentsCandles(sym, params)
            r = client.request(r)
            for p in r['candles']:
                dtime = datetime.strftime(datetime.strptime(
                    p['time'][0:10], '%Y-%m-%d') + timedelta(days=1), '%Y-%m-%d')
                price = round((float(p['mid']['o']) + float(p['mid']['h']) + float(
                    p['mid']['l']) + float(p['mid']['c'])) / 4, len(p['mid']['c'].split('.')[1]))
                chang = round(
                    (float(p['mid']['c']) / float(p['mid']['o']) - 1) * 100, 2)
                volat = round(
                    (float(p['mid']['h']) / float(p['mid']['l']) - 1) * 100, 2)
                prices[sym][dtime] = price
                changs[sym][dtime] = chang
                volats[sym][dtime] = volat

        # clean nans
        for sym in symbols:
            changs[sym] = changs[sym].fillna(0)
            volats[sym] = volats[sym].fillna(0)
            for i in range(len(prices.index)):
                if isnan(prices[sym][i]):
                    try:
                        prices[sym][i] = prices[sym][i-1]
                    except:
                        prices[sym][i] = prices[sym][i+1]

        # create db
        path = 'db/instruments/'+str(y)+'/'
        Path(path).mkdir(parents=True, exist_ok=True)
        prices.to_csv(path+'prices.csv', index=True)
        changs.to_csv(path+'changs.csv', index=True)
        volats.to_csv(path+'volats.csv', index=True)

        print(y, ' upadted!')

        y += 1


if __name__ == '__main__':
    importdb(int(sys.argv[1]), symbols)
    print('history db updated!')
