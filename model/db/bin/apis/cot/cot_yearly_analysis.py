# cot_yearly_analysis.py

# Compute and plot net positions for speculators and commercials in EUR/USD Futures against weekly spot equivalent.
# This script should be executed after the cot_downloader.py, otherwise unzip individual CoT reports manually

import os
import pandas as pd

from plotters import generic_time_series
from pathlib import Path


columns = [
    'Market and Exchange Names',
    'As of Date in Form YYYY-MM-DD',
    'Noncommercial Positions-Long (All)',
    'Noncommercial Positions-Short (All)',
    'Noncommercial Positions-Spreading (All)',
    'Commercial Positions-Long (All)',
    'Commercial Positions-Short (All)',
    'Nonreportable Positions-Long (All)',
    'Nonreportable Positions-Short (All)'
]

def net_positions(instrument):
    """ Computes the net position for large speculators and hedgers, where,

        net_position = long - short
    """
    large_speculators_net_position = instrument[2] - instrument[3]
    hedgers_net_position = instrument[5] - instrument[6]
    return large_speculators_net_position, hedgers_net_position

def market_sentiment(instrument):
    """ Compute market sentiment from Commitment of Traders report, where,

        instrument: is a list
        market sentiment = speculators net position - commercials net position
        market net position = long - short
    """
    non_commercials_net_position, commercials_net_position = net_positions(instrument)
    return non_commercials_net_position - commercials_net_position

def speculators_sentiment(instrument):
    """ Compute speculator position from CoT report, where,

        instrument: is a list
        speculators_long = # speculators long / (# spec. long + # spec. short)
        speculators_short = # speculators short / (# spec. long + # spec. short)
    """
    speculators_long = instrument[2] / (instrument[2] + instrument[3])
    speculators_short = instrument[3] / (instrument[2] + instrument[3])
    return round(speculators_long, 4), round(speculators_short, 4)

if __name__ == '__main__':
    data_sets = Path.cwd() / 'data-sets'
    cot_reports = data_sets / 'commitments-of-traders'       # this folder is created in cot_downloader.py


    market_data = pd.read_csv(Path.cwd() / cot_reports / 'deacot2019' / 'annual.txt', delimiter=',', usecols=columns)
    # market_data = pd.read_csv(Path.cwd() / cot_reports / 'deacot2018' / 'annual.txt', delimiter=',', usecols=columns)
    speculators = []
    hedgers = []
    for market in market_data.values:
        if 'EURO FX ' in market[0]:                          # you can use any FX pair here, I used EUR/USD future
            market_delta = market_sentiment(market)
            speculators_net_position, hedgers_net_position = net_positions(market)
            speculators_long, speculators_short = speculators_sentiment(market)
            speculators.append((market[1], speculators_net_position, speculators_long, speculators_short))
            hedgers.append((market[1], hedgers_net_position))

            print(f"week: {market[1]} (Tuesday)")
            print(f'market sentiment: {market_delta}')
            print(
                'large speculators:',
                f'net position = {speculators_net_position},',
                f'long = {speculators_long} %,',
                f'short = {speculators_short} % \n',
            )

    # I'm using the weekly EUR/USD spot data -- it doesn't really matter what pair, so long the spot pair is consistent with
    # the future pair
    eur_usd = pd.read_csv(eur_usd_weekly_spot / 'EURUSD_Candlestick_1_W_BID_31.12.2018-30.11.2019.csv')
    # eur_usd = pd.read_csv( eur_usd_weekly_spot / 'EURUSD_Candlestick_1_W_BID_31.12.2017-31.12.2018.csv')
    eur_usd['Local time'] = sorted(pd.to_datetime(eur_usd['Local time']))
    weeks = pd.to_datetime([net_position[0] for net_position in speculators])
    generic_time_series(
        eur_usd['Local time'],
        eur_usd['Close'],
        filename='EUR_USD_2018_weekly',
        plot_title='EUR/USD weekly spot rate in 2019',
        multi=True,
        extra_x=weeks,
        extra_y_1=[net_position[1] for net_position in speculators],
        extra_y_2=[net_position[1] for net_position in hedgers],
        extra_y_1_legend_label='Speculators net position',
        extra_y_2_legend_label='Hedgers net position',
        extra_y_1_hover_tool=[net_position[2] for net_position in speculators],
        extra_y_2_hover_tool=[net_position[3] for net_position in speculators]
    )