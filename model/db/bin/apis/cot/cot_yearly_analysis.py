# cot_yearly_analysis.py

# Compute and plot net positions for speculators and commercials in EUR/USD Futures against weekly spot equivalent.
# This script should be executed after the cot_downloader.py, otherwise unzip individual CoT reports manually

import os
import pandas as pd

from pathlib import Path


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

def compute_history():

    data_sets = Path.cwd() / 'model/db/bin/apis/cot/'
    cot_reports = data_sets / 'cots_raw'       # this folder is created in cot_downloader.py
    speculators = []
    hedgers = []
    for year in range(2005, 2023):
        print(year)
        market_data = pd.read_csv(Path.cwd() / cot_reports / f'deacot{str(year)}' / 'annual.txt', delimiter=',', usecols=columns)
        # market_data = pd.read_csv(Path.cwd() / cot_reports / 'deacot2018' / 'annual.txt', delimiter=',', usecols=columns)
        for market in market_data.values:
            if 'EURO FX ' in market[0]:
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
        
    weeks = pd.to_datetime([net_position[0] for net_position in speculators])
    
    return speculators

compute_history()