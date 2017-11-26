import pprint
import requests
import pandas as pd
from pandas.io.json import json_normalize
from src.secrets import DATABASE, COLLECTION, API_KEY
import json

#http://docs.mlab.com/data-api/
URL = f"https://api.mlab.com/api/1/databases/{DATABASE}/collections/{COLLECTION}?apiKey="


def main():
    x = requests.get(URL + API_KEY).json()
    df = json_normalize(x)
    df['mmol'] = df.sgv / 18 # mmol/l = mg/dl / 18
    df['date1'] = pd.to_datetime(df.dateString)
   # df['date1'] = df.date1.dt.strftime('yyyy-mm-dd')
    print(df.head())
    #df = pd.read_json(list(x), orient="index")
    #pprint.pprint(x)
    #print(df.head())



if __name__ == '__main__':
    main()
