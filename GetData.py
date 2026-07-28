import yfinance as yf
from datetime import datetime, timedelta

import requests
import pandas as pd
from io import StringIO

#import Scalp

def get_500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    print(url)

    

    try:
        response = requests.get(url,headers={"User-Agent": "Mozilla/5.0"})

        response.raise_for_status()

        tables = pd.read_html(StringIO(response.text))

        sp500 = tables[0]
        tickers = sp500["Symbol"].tolist()

        return tickers

    except Exception as error:
        print("erreur")
        print(f"error : {error}")
        return [] # return an empty list to no break anything



allTickers = get_500_tickers()
