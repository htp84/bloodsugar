from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import plotly.graph_objs as go
import datetime
import json
import pandas as pd
import numpy as np
import plotly
from apps.src.data import data, bloodsugar_describe
from apps.src.fig import scatter_, histogram_#, histogram__
from apps.src.html_style import style_
from apps.src.secrets import CONN_STR
import base64
from app import app

style = {'padding': '5px', 'fontSize': '16px', 'color': 'red'}
startdate = datetime.date.today() - datetime.timedelta(days=14)
df = data(CONN_STR, startdate=str(startdate))
dateparts = ['minute', 'hour', 'day', 'week', 'month', 'quarter', 'year']
graphs = ['scatter', 'histogram']
df1 = bloodsugar_describe(df, 'week')
#print(df1.head())
dfb = data(CONN_STR, latest=True)
blood_sugar = dfb.at[0, 'mmol']
style = style_(blood_sugar)
time = dfb.at[0, 'min_diff']
style_time= style_()

layout = html.Div([
    html.H4('Blodsocker'),
    html.Div(
        [html.Span('Blodsocker: {0:.2f}'.format(blood_sugar), style=style)],
    id='current-bloodsugar',    
    ),
    html.Div(
        [html.Span('Tid: {0:.2f}'.format(time), style=style_time)],
    id='time-since-update',
    ),
    dcc.Dropdown(
        id='dropdown-datepart',
        options=[{'label': i, 'value': i}
                  for i in dateparts],
        value='week'
    ),
    dcc.Input(
        id='input-startdate',
        type='Date',
        value=datetime.date.today() - datetime.timedelta(days=14)
    ),
    dcc.Dropdown(
        id='dropdown-graph',
        options=[{'label': i, 'value': i}
                  for i in graphs],
        value='scatter'
    ),
    html.Div([
        dcc.Graph(
            id='graph-bloodsugar-describe',
            hoverData={'points': [{'customdata': 'Japan'}]},
            figure=scatter_(df)
        )
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
            dt.DataTable(
            rows = df1.to_dict('records'),

            columns = ['date1', 'mean', 'std', 'min', '25%', '50%', '75%', 'max', 'count'],

            row_selectable=False,
            filterable=True,
            sortable=True,
            selected_row_indices=[],
            id='datatable-bloodsugar-describe',
            min_height=1000,
            min_width=1000
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    #html.Div([html.Img(histogram__(df))],
    #id='hist-test'),
    dcc.Interval(
        id='interval-component',
        interval=1*40000#60000 # in milliseconds
    ), dcc.Link('Go to App 2', href='/apps/app2')
], className="container")

@app.callback(Output('current-bloodsugar', 'children'),
              events=[Event('interval-component', 'interval')])
def update_blood():
    df = data(CONN_STR, latest=True)
    blood_sugar = df.at[0, 'mmol']
    if blood_sugar >= 10:
        style = {'padding': '20px', 'fontSize': '32px', 'background-color': 'red'}
    elif 4 <= blood_sugar < 10:
        style = {'padding': '20px', 'fontSize': '32px', 'background-color': 'green'}
    else:
        style = {'padding': '20px', 'fontSize': '32px', 'background-color': 'pink'}
    return [
        html.Span('Blodsocker: {0:.2f}'.format(blood_sugar), style=style)
    ]


@app.callback(Output('time-since-update', 'children'),
              events=[Event('interval-component', 'interval')])
def update_time():
    df = data(CONN_STR, latest=True) 
    time = df.at[0, 'min_diff']
    style = {'padding': '20px', 'fontSize': '20px', 'background-color': 'grey', "display": "inline-block"}
    return [
        html.Span('Tid: {0:.2f}'.format(time), style=style),
    ]

@app.callback(
    Output('graph-bloodsugar-describe', 'figure'),
    [Input('input-startdate', 'value'),
    Input('dropdown-graph', 'value')],
    events=[Event('interval-component', 'interval')])
def update_graph(startdate, graph):
    df = data(CONN_STR, startdate=str(startdate))
    if graph == 'histogram':
        return histogram_(df)
    else:
        return scatter_(df)

@app.callback(
    Output('datatable-bloodsugar-describe', 'rows'),
    [Input('dropdown-datepart', 'value'),
    Input('input-startdate', 'value')],
    events=[Event('interval-component', 'interval')])
def update_table(datepart, startdate):
    #print(startdate)
    df = data(CONN_STR)
    rows = bloodsugar_describe(df, datepart, startdate=str(startdate)).to_dict('records')
    return rows
