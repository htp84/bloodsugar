import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import datetime
import json
import pandas as pd
import numpy as np
import plotly
from src.data import data, bloodsugar_describe
from src.secrets import CONN_STR

app = dash.Dash()
app.scripts.config.serve_locally = True

df = data(CONN_STR)
dateparts = ['minute', 'hour', 'day', 'week', 'month', 'quarter', 'year']
df1 = bloodsugar_describe(df, 'hour')
#print(df1.head())

app.layout = html.Div([
    html.H4('Blodsocker'),
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
    ),
    html.Div(id='selected-indexes'),
    dcc.Graph(
        id='graph-bloodsugar-describe'
    ),
], className="container")

@app.callback(
    dash.dependencies.Output('datatable-bloodsugar-describe', 'rows'),
    [dash.dependencies.Input('dropdown-datepart', 'value'),
    dash.dependencies.Input('input-startdate', 'value')])
def update_table(datepart, startdate):
    print(startdate)
    rows = bloodsugar_describe(df, datepart, startdate=str(startdate)).to_dict('records')
    return rows

app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

if __name__ == '__main__':
    app.run_server(debug=True)


