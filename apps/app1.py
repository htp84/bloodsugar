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
        [html.Span('Blodsocker: ')],
    id='current-bloodsugar'
    ),
    html.Div(
        [html.Span(f'Tid: min', style=style_time)],
    id='time-since-update',
    ),
    html.Label('Timmar'),
    dcc.RadioItems(
        options=[
            {'label': '1h', 'value': 1},
            {'label': '3h', 'value': 3},
            {'label': '6h', 'value': 6},
        ],
        value=6,
        id='radio-amount'
    ),
    html.Label('Text Input'),
    dcc.Input(value='', type='text', id='text-amount'),
    html.Div([
        dcc.Graph(
            id='graph-bloodsugar',
            hoverData={'points': [{'customdata': 'Japan'}]}
            #figure=scatter_(df)
        )
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),
    dcc.Interval(
        id='interval-component',
        interval=1*60000 # in milliseconds
    ), dcc.Link('Go to App 2', href='/apps/app2')
], className="container")

@app.callback(Output('current-bloodsugar', 'children'),
              [Input('radio-amount', 'value')],
              events=[Event('interval-component', 'interval')])
def update_blood(update):
    df = data(CONN_STR, latest=True)
    blood_sugar = df.at[0, 'mmol']
    style = style_(blood_sugar)
    return [
        html.Span('Blodsocker: {0:.2f}'.format(blood_sugar), style=style)
    ]


@app.callback(Output('time-since-update', 'children'),
              [Input('radio-amount', 'value')],
              events=[Event('interval-component', 'interval')])
def update_time(update):
    df = data(CONN_STR, latest=True) 
    time = df.at[0, 'min_diff']
    return [
        html.Span(f'Tid: {time} min', style=style_time),
    ]

@app.callback(
    Output('graph-bloodsugar', 'figure'),
    [Input('radio-amount', 'value'),
    Input('text-amount', 'value')],
    events=[Event('interval-component', 'interval')])
def update_graph(hours_radio=None, hours_text=None):
    if hours_text:
        try:
            hours_text = int(hours_text)
            df = data(CONN_STR, time_unit='h', amount=int(hours_text))
        except:
            df = data(CONN_STR, time_unit='h', amount=hours_radio)
    else:
        df = data(CONN_STR, time_unit='h', amount=hours_radio)
    return scatter_(df)


