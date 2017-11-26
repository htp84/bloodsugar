import pprint
import requests
from src.secrets import DATABASE, COLLECTION, API_KEY

#http://docs.mlab.com/data-api/
URL = f"https://api.mlab.com/api/1/databases/{DATABASE}/collections/{COLLECTION}?apiKey="


def main():
    x = requests.get(URL + API_KEY).json()
    pprint.pprint(x)



if __name__ == '__main__':
    main()
