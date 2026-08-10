#for the get_500_tickers()
import requests
import pandas as pd
from io import StringIO

# for the algo
import Request
import random

random.seed(0)


def get_500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    #print(url)

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


def choose_purchase( current_date):
    allTickers = get_500_tickers()
    random_ticker = random.choice(allTickers)

    tickerData = Request.get_ticker_stock(random_ticker)

    #in week
    if current_date.strftime("%A") not in ("Saturday", "Sunday"):
        price = Request.get_stock_price(current_date, tickerData)


        #unexpected closure
        if price == None :
            print("4")
            print("Market close that day")
            return None
            
        else:
            Request.purchase_open_stock(current_date, tickerData)
            

    # in weekend
    else:
        print("Market close for weekend")
        return None
        
    #price = Request.get_stock_price(current_date,tickerData)

    return tickerData
    
