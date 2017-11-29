"""jhkk
"""
from datetime import datetime
from pymongo import MongoClient
from pprint import pprint
import requests
import pandas as pd
from pandas.io.json import json_normalize

def data(CONN_STR):
    """ghjghj
    """
    client = MongoClient(CONN_STR)
    db = client.heroku_dc8bxz64
    entries = db.entries
    all_data = list(entries.find())
    #print(all_data)
    #pprint(db.collection_names(include_system_collections=False))
    df = json_normalize(all_data)
    return df


def bloodsugar_describe(df: pd.DataFrame, datepart: str, **kwargs):
    """Creates a summary table for the bloodsugar values
    
    Parameters
    ----------
    df : dataframe, must include columns date1 [datetime] and mmol [float]
    datepart : str, datepart e.g. 'hour', 'day', 'week', 'month', 'quarter'
    
    Keyword arguments
    -----------------
    all_data : bool, if set to True the summary table include all data. if all_data,
            start and/or end are given all_data overwrites start and end.               
    amount : int, set the amount of 
    time_unit : str,
    start : datetime,
    end : datetime,
    """
    df['mmol'] = df.sgv / 18 # mmol/l = mg/dl / 18
    df['date1'] = pd.to_datetime(df.dateString)
    df['date1'] = pd.to_datetime(df.dateString)
    df.date1 = df.date1.astype(datetime)
    x = pd.to_timedelta(1, 'h')
    df.date1 = df.date1 + x
    df.sort_values('date1', ascending=1, inplace=True)
    all_data = kwargs.pop('all_data', False)
    amount = kwargs.pop('amount', 14)
    time_unit = kwargs.pop('time_unit', 'd')
    delta = pd.to_timedelta(amount, time_unit)
        
    start = kwargs.pop('start', df.date1.max() - delta)
    end = kwargs.pop('stop', df.date1.max())
    
    if not all_data:
        df = df[(df['date1'] > start) & (df['date1'] <= end)]

    df2 = pd.DataFrame()
    
    df2['mean'] = df.groupby(getattr(df.date1.dt, datepart))['mmol'].mean()
    df2['std'] = df.groupby(getattr(df.date1.dt, datepart))['mmol'].std()
    df2['median'] = df.groupby(getattr(df.date1.dt, datepart))['mmol'].median()
    df2['75%'] = df.groupby(getattr(df.date1.dt, datepart))['mmol'].quantile(0.75)
    df2['25%'] = df.groupby(getattr(df.date1.dt, datepart))['mmol'].quantile(0.25)
    df2['min'] = df.groupby(getattr(df.date1.dt, datepart))['mmol'].min()
    df2['max'] = df.groupby(getattr(df.date1.dt, datepart))['mmol'].max()
    df2['count'] = df.groupby(getattr(df.date1.dt, datepart))['mmol'].count()
    
        
    return df2.reset_index()
