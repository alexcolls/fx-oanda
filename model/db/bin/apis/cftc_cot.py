
# CFTC COT FUTURS & OPTIONS REPORTS

# author: Quantium Rock
# date: August 2022
# license: MIT

# Download all available CoT FuturesOnly reports from CFTC website

import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path
from zipfile import ZipFile
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.io import output_file
from bokeh.layouts import column



def cot_bulk_downloader():
    """ Downloads all standard Commitment of Traders Futures only reports. """
    url = 'https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm'
    out_path = Path.cwd() / 'data-sets' / 'commitments-of-traders'
    if out_path.exists():  # avoid re-downloading the script if the files have already been downloaded
        return 0
    os.makedirs(out_path, exist_ok=True)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for name in soup.findAll('a', href=True):
        file_url = name['href']
        if file_url.endswith('.zip'):
            filename = file_url.split('/')[-1]
            if 'deacot' in filename:
                out_name = out_path.joinpath(filename)
                zip_url = 'https://www.cftc.gov/files/dea/history/' + filename
                req = requests.get(zip_url, stream=True)
                if req.status_code == requests.codes.ok:
                    print(f'Downloading {filename} . . .')
                    with open(out_name, 'wb') as f:
                        for chunk in req.iter_content():
                            if chunk:  # ignore keep-alive requests (?)
                                f.write(chunk)
                        f.close()

    print('Finished downloading reports')
    return 0

def bulk_unzipper(directory):
    """ Unzips all archives within the CoT directory. """
    for file in directory.iterdir():
        if str(file).endswith('.zip'):
            print(f'Unzipping {file} . . .')
            with ZipFile(file, 'r') as zip_object:
                filename = zip_object.filename.split('/')[-1]  # after split consider only the 'deacotXXXX.zip part
                filename = filename.split('.zip')[0]           # consider only the 'deacotXXXX' string
                zip_object.extractall(directory / filename)
    return 0



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
    eur_usd_weekly_spot = data_sets / 'eur-usd-weekly-spot'
    os.makedirs(eur_usd_weekly_spot, exist_ok=True)

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


def generic_time_series(x, y, filename='', **kwargs):
    """ Plots a time-series. """

    # plot data and canvas settings
    p = figure(plot_width=1440, plot_height=650, x_axis_type='datetime')
    p.line(x, y, color='orange', line_width=4.0, legend_label=kwargs.get('main_legend_label', filename))
    if 'mean' in kwargs:
        mean = kwargs['mean']
        mean_series = [mean for _ in range(len(y))]
        p.line(x, mean_series, color='blue', line_width=1.5, legend_label='Mean')
    if 'multi' in kwargs:
        if kwargs['multi']:
            source = ColumnDataSource(data=dict(
                x=kwargs['extra_x'],
                y_1 = kwargs['extra_y_1'],
                y_2 = kwargs['extra_y_2'],
                extra_y_1_hover_tool=kwargs['extra_y_1_hover_tool'],
                extra_y_2_hover_tool=kwargs['extra_y_2_hover_tool']
            ))

            extra_figure = figure(plot_width=1440, plot_height=150, x_axis_type='datetime')
            extra_figure.line(
                'x',
                'y_1',
                source=source,
                color='darkred',
                line_width=4.0,
                legend_label=kwargs.get('extra_y_1_legend_label', 'Extra 1')
            )
            extra_figure.line(
                'x',
                'y_2',
                source=source,
                color='navy',
                line_width=4.0,
                legend_label=kwargs.get('extra_y_2_legend_label', 'Extra 2')
            )
            # styling
            extra_figure.toolbar_location = None
            extra_figure.left[0].formatter.use_scientific = False
            extra_figure.legend.location = 'center_left'
            hover = HoverTool(
                tooltips=[
                    ('Date', '@x{%d-%m-%Y}'),
                    ('Speculators long', '@{extra_y_1_hover_tool}'),
                    ('Speculators short', '@{extra_y_2_hover_tool}'),
                ],
                formatters={
                    'x': 'datetime'
                }
            )
            extra_figure.tools = [hover]

    # plot styling
    p.title.text = kwargs.get('plot_title', filename)
    p.title.align = 'center'
    p.toolbar_location = None
    p.outline_line_color = None
    # p.xgrid[0].ticker.desired_num_ticks = 10
    p.xgrid.grid_line_color = None
    hover = HoverTool(
        tooltips=[
            ('Date', '@x{%d-%m-%Y}'),
            ('Rate:', '@y'),
        ],
        formatters={
            'x': 'datetime'
        }
    )
    p.tools = [hover]
    p.legend.location = 'top_right'
    p.legend.border_line_color = 'navy'
    p.legend.border_line_alpha = 0.4
    p.legend.border_line_width = 2

    # save plot to file and render
    output_dir = Path.cwd() / 'plots'
    os.makedirs(output_dir, exist_ok=True)
    output_file('plots/{}.html'.format(filename))
    if 'multi' in kwargs:
        if kwargs['multi']:
            show(column(p, extra_figure))
    else:
        show(p)

if __name__ == '__main__':
    try:
        return_val = cot_bulk_downloader()
        if return_val == 0:  # hunky-dory so proceed to unzip
            cot_dir = Path.cwd() / 'data-sets' / 'commitments-of-traders'  # path created by bulk downloader so no I/O error 
            bulk_unzipper(cot_dir)
    except Exception as exception:
        print(f'Unexpected error: {exception}')