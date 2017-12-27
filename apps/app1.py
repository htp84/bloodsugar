from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import plotly.graph_objs as go
import pandas as pd
import plotly
from apps.src.data import data, bloodsugar_describe
from apps.src.fig import scatter_#, histogram__
from apps.src.html_style import style_
from apps.src.secrets import CONN_STR
import datetime
from app import app

style_time= style_()

layout = html.Div([
    html.H4('Blodsocker'),
    html.Div(
        [html.Span('Blodsocker: {0:.2f}'.format(data(CONN_STR, latest=True).at[0, 'mmol']), style=style_(data(CONN_STR, latest=True).at[0, 'mmol']))],
    id='current-bloodsugar',    
    ),
    html.Div(
        [html.Span('Tid: {0:.2f}'.format(data(CONN_STR, latest=True).at[0, 'min_diff']), style=style_time)],
    id='time-since-update',
    ),
    html.Div([
        dcc.Graph(
            id='graph-bloodsugar-describe',
            figure=scatter_(data(CONN_STR, startdate=str(datetime.date.today() - datetime.timedelta(days=1))))
        )
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),
    dcc.Interval(
        id='interval-component',
        interval=1*60000 # in milliseconds
    ), dcc.Link('Go to App 2', href='/apps/app2')
], className="container")

@app.callback(Output('current-bloodsugar', 'children'),
              events=[Event('interval-component', 'interval')])
def update_blood():
    df = data(CONN_STR, latest=True)
    blood_sugar = df.at[0, 'mmol']
    style = style_(blood_sugar)
    return [
        html.Span('Blodsocker: {0:.2f}'.format(blood_sugar), style=style)
    ]


@app.callback(Output('time-since-update', 'children'),
              events=[Event('interval-component', 'interval')])
def update_time():
    df = data(CONN_STR, latest=True) 
    time = df.at[0, 'min_diff']
    return [
        html.Span('Tid: {0:.2f}'.format(time), style=style_time),
    ]

@app.callback(
    Output('graph-bloodsugar-describe', 'figure'),
    events=[Event('interval-component', 'interval')])
def update_graph():
    startdate = str(datetime.date.today() - datetime.timedelta(days=1))
    df = data(CONN_STR, startdate=startdate)
    return scatter_(df)


