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
        
    start = kwargs.pop('startdate', df.date1.max() - delta)
    end = kwargs.pop('stopdate', df.date1.max())
    
    if not all_data:
        df = df[(df['date1'] > start) & (df['date1'] <= end)]
    
    df = df.groupby(getattr(df.date1.dt, datepart))['mmol'].describe().reset_index().round(2)

        
    return df
