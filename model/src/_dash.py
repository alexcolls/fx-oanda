
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

from src.functions import LowPass


years = [ 2022, 2021, 2020, 2019 ]
weeks = range( 1, 52 )

# create the Dash app
app = dash.Dash('Model Dashboard')

params = [ 'Year', 'Week' ]

# set up the app layout
app.layout = html.Div(style={ 'margin': '80px'} ,children=[

    html.H1(children='MODEL DASHBOARD'),

    html.H3(children='Select year: '),

    dcc.Dropdown(id='year', options=[{'label': yr, 'value': yr} for yr in years], value='2019'),

    html.H3(children='Select week: '),

    dcc.Dropdown(id='week', options=[{'label': wk, 'value': wk} for wk in weeks], value='1'),

    html.H2(style={ 'margin-top': '50px'}, children='Market returns (%)'),

        dcc.Graph(id='chart-mids'),

        html.H3(children='Spreads (%%) pips'),

        dcc.Graph(id='chart-spreads'),

        html.H3(children='Raw trading volumes'),

        dcc.Graph(id='chart-volumes'),

    html.H2(children='Dimensional reduction to currency indexes (%)'),

        html.H4(children='Low Pass filter applied (ccy_lp)'),

        dcc.Graph(id='chart-idxs'),

        #dcc.Slider(id='filter_order'),
        #dcc.Slider(id='cutoff_freq'),

        html.H3(children='White noise / High frequencies (%)'),

        dcc.Graph(id='chart-noise'),

        html.H3(children='Trend momentum (LP slope)'),

        dcc.Graph(id='chart-trend'),
])

# set up callback function
@ app.callback(

    Output(component_id='chart-mids', component_property='figure'),
    Output(component_id='chart-spreads', component_property='figure'),
    Output(component_id='chart-volumes', component_property='figure'),

    Output(component_id='chart-idxs', component_property='figure'),
    Output(component_id='chart-noise', component_property='figure'),

    Output(component_id='chart-trend', component_property='figure'),

    Input(component_id='year', component_property='value'),
    Input(component_id='week', component_property='value'),

    #Input(component_id='filter_order', component_property='value'),
    #Input(component_id='cutoff_freq', component_property='value')

)
def selectWeek( year, week, filter_order=8, cutoff_freq=0.01  ):

    # plot mids returns
    mids_ = pd.read_csv('db/data/secondary/' + str(year) +'/'+ str(week) +'/'+ 'mids_.csv', index_col=0)
    mids_plt = px.line(mids_, height=800)

    # plot spreads (%%) pips
    spreads_ = pd.read_csv('db/data/primary/' + str(year) +'/'+ str(week) +'/'+ 'spreads.csv', index_col=0)
    spreads_.index = pd.to_datetime(spreads_.index)
    spreads_plt = px.line(spreads_, height=400)

    # plot raw volumes
    volumes_ = pd.read_csv('db/data/primary/' + str(year) +'/'+ str(week) +'/'+ 'volumes.csv', index_col=0)
    volumes_plt = px.line(volumes_, height=400)

    # plot idxs returns
    idxs_ = pd.read_csv('db/data/secondary/' + str(year) +'/'+ str(week) +'/'+ 'idxs_.csv', index_col=0)

    lowpass_, idxs_lp = LowPass( idxs_, filter_order, cutoff_freq  )

    """
        ln = 60
        for i in range(ln, len(idxs_)):
            
            lowpass_i, _ = LowPass( idxs_.iloc[:i], filter_order, cutoff_freq  )
            lowpass_i = lowpass_i[0, :]

            for ccy in idxs_.columns:
                
                idxs_lp[ccy+'_rt'][i] = lowpass_i[ccy].iloc[0]

    """

    idxs_plt = px.line( idxs_lp, height=800)

    noise_ = idxs_ - lowpass_
    noise_plt = px.line(noise_, height=600)

    """
    # plot idxs returns
    mom_ = pd.DataFrame(index=idxs_.index, columns=idxs_.columns)

    for i in range(2, len(idxs_)):
        for ccy in idxs_.columns:
            mom_[ccy][i] = ( idxs_[ccy][i] - idxs_[ccy][i-1] )

    mom_plt = px.line(mom_, height=400)

    """

    # trend
    trend_ = pd.DataFrame(index=idxs_.index, columns=idxs_.columns)

    for i in range(2, len(idxs_)):
        for ccy in idxs_.columns:
            trend_[ccy][i] = ( lowpass_[ccy][i] - lowpass_[ccy][i-1] )

    trend_plt = px.line(trend_, height=600)
    

    return mids_plt, spreads_plt, volumes_plt, idxs_plt, noise_plt, trend_plt



# run local server
if __name__ == '__main__':
    app.run_server(debug=True)