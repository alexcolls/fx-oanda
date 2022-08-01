
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from os import listdir


def read_indexes(timeframe):
    files = [k for k in listdir('db/indexes/'+timeframe)]
    df = pd.read_csv('db/indexes/'+timeframe+'/'+currencies[0])
    df[files[0]] = df[files[0]].cumsum()
    for i in range(1, len(currencies)):
        df2 = pd.read_csv('db/indexes/'+timeframe+'/'+currencies[0]+'.csv')
        df2[currencies[i]] = df2[currencies[i]].cumsum()
        df = pd.merge(df, df2, on=['date', 'date'])
    df = df.set_index('date')
    return df


# create the Dash app
app = dash.Dash()


# set up the app layout
app.layout = html.Div(children=[
    html.H1(children='FX G10 Currency Strategy'),
    dcc.Dropdown(id='timeframe-dropdown', options=[{'label': i, 'value': i}
                 for i in ['W', 'D', 'H8', 'H4', 'H1', 'M15']], value='D1'),
    dcc.Graph(id='idx-chart'),
    dcc.Slider(id='lowpass-slider')
])


# set up callback function
@ app.callback(
    Output(component_id='idx-chart', component_property='figure'),
    Input(component_id='timeframe-dropdown', component_property='value')
)
def update_graph(timeframe):
    df = read_indexes(timeframe)
    graph = px.line(df, height=900)
    graph.update_layout(xaxis_type='category')
    return graph


# run local server
if __name__ == '__main__':
    app.run_server(debug=True)
