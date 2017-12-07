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
from apps.src.fig import scatter_, histogram_, boxplot_
from apps.src.html_style import style_
from apps.src.secrets import CONN_STR

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
dateparts = ['minute', 'hour', 'weekday', 'day', 'week', 'month', 'quarter', 'year']

layout = html.Div([
    dcc.Input(
        id='input-startdate',
        type='Date',
        value=datetime.date.today() - datetime.timedelta(days=14)
    ),
    html.Div([
        dcc.Graph(
            id='graph-bloodsugar-histogram',
            figure=histogram_(df)
        )
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),
    dcc.Dropdown(
        id='dropdown-datepart',
        options=[{'label': i, 'value': i}
                  for i in dateparts],
        value='week'
    ),
    html.Div([
        dcc.Graph(
            id='graph-bloodsugar-scatter',
            figure=boxplot_(df, datepart='week')
        )
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),
        dcc.Link('Go to App 1', href='/apps/app1')
], className="container")

@app.callback(
    Output('graph-bloodsugar-histogram', 'figure'),
    [Input('input-startdate', 'value')])
def update_hist(startdate):
    df = data(CONN_STR, startdate=str(startdate))
    return histogram_(df)
@app.callback(
    Output('graph-bloodsugar-scatter', 'figure'),
    [Input('input-startdate', 'value'),
    Input('dropdown-datepart', 'value')])
def update_scatt(startdate, datepart):
    df = data(CONN_STR, startdate=str(startdate))
    return boxplot_(df, datepart=datepart)





#@app.callback(
#    Output('datatable-bloodsugar-describe', 'rows'),
#    [Input('dropdown-datepart', 'value'),
#    Input('input-startdate', 'value')])
#def update_table(datepart, startdate):
#    #print(startdate)
#    df = data(CONN_STR)
#    rows = bloodsugar_describe(df, datepart, startdate=str(startdate)).to_dict('records')
#    return rows