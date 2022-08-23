
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
pd.options.plotting.backend = "plotly"
import plotly.express as px

years = [ 2019, 2020, 2021, 2022 ]
weeks = range( 1, 52 )

# create the Dash app
app = dash.Dash('Model Dashboard')

params = [ 'Year', 'Week' ]

# set up the app layout
app.layout = html.Div(style={ 'margin': '100px'} ,children=[

    html.H1(children='MODEL DASHBOARD'),

    html.H3(children='Select year: '),

    dcc.Dropdown(id='year', options=[{'label': yr, 'value': yr} for yr in years], value='2019'),

    html.H3(children=f'Select week: '),

    dcc.Dropdown(id='week', options=[{'label': wk, 'value': wk} for wk in weeks], value='1'),


    html.H2(style={ 'margin-top': '100px'}, children='Portfolio returns (%)'),

        dcc.Graph(id='chart-mids'),

        html.H3(children='Spreads (%%) pips'),

        dcc.Graph(id='chart-spreads'),

        html.H3(children='Raw trading volumes'),

        dcc.Graph(id='chart-volumes'),

    html.H2(children='Dimensional reduction to currency indexes (%)'),

        

    html.H2(children=f'Apply Low Pass filter (%)'),

    dcc.Slider(id='lowpass-slider'),

])

# set up callback function
@ app.callback(

    Output(component_id='chart-mids', component_property='figure'),
    Output(component_id='chart-spreads', component_property='figure'),

    Output(component_id='chart-volumes', component_property='figure'),

    Input(component_id='year', component_property='value'),
    Input(component_id='week', component_property='value')
)
def selectWeek( year, week ):

    # plot mids returns
    mids_ = pd.read_csv('db/data/primary/' + str(year) +'/'+ str(week) +'/'+ 'mids.csv', index_col=0)
    mids_.index = pd.to_datetime(mids_.index)
    mids_ = px.line(mids_, height=800)

    # plot spreads (%%) pips
    spreads_ = pd.read_csv('db/data/primary/' + str(year) +'/'+ str(week) +'/'+ 'spreads.csv', index_col=0)
    spreads_.index = pd.to_datetime(spreads_.index)
    spreads_ = px.line(spreads_, height=400)

    # plot ccys returns
    idxs_ = pd.read_csv('db/data/primary/' + str(year) +'/'+ str(week) +'/'+ 'volumes.csv', index_col=0)
    idxs_.index = pd.to_datetime(idxs_.index)
    idxs_ = px.line(idxs_, height=400)
    #graph.update_layout(xaxis_type='category')
    return mids_, spreads_, idxs_


# run local server
if __name__ == '__main__':
    app.run_server(debug=True)