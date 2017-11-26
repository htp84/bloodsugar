from pymongo import MongoClient
import pprint
import requests
import pandas as pd
from pandas.io.json import json_normalize
from src.secrets import CONN_STR
import json

#http://docs.mlab.com/data-api/



def main():
    client = MongoClient(CONN_STR)
    db = client.heroku_dc8bxz64
    entries = db.entries
    all_data = list(entries.find())
    #print(all_data)
    #pprint.pprint(db.collection_names(include_system_collections=False))
    df = json_normalize(all_data)
    df['mmol'] = df.sgv / 18 # mmol/l = mg/dl / 18
    df['date1'] = pd.to_datetime(df.dateString)
    print(df.head())



if __name__ == '__main__':
    main()
