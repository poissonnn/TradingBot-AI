import yfinance as yf
from datetime import datetime, timedelta

from collections import defaultdict

import requests
import pandas as pd
from io import StringIO
import pytz # pour être sur la bourse américaine

new_york_now = datetime.now(pytz.timezone("America/New_York")).hour
print(f"New york hours : {new_york_now}")


#get all the information about a ticker
def get_ticker_stock(ticker, period = "max", interval = "1d"):

    #print("hi from scalp")

    ticker = yf.Ticker(ticker)
    info = ticker.history(period=period, interval=interval)
    #print(info)

    return info

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

def get_purchase_history():

    all_purchase = defaultdict(list)

    with open("purchaseHistory.txt") as purchaseHistory:
        lines = purchaseHistory.readlines()

    fileLength = len(lines)

    for i in range(fileLength):
        #take the line
        stockPurchase = lines[i].strip()
        stockPurchase = stockPurchase.split() # split each element separated by a space

        #print(stockPurchase)
        ticker = stockPurchase[1]
        ticker = ticker.strip()
    
        date = stockPurchase[0]
        date = date.strip()

        all_purchase[ticker].append(date)

    all_purchase = dict(all_purchase)

    return all_purchase

def get_stock_price(time, tickerData, atOpeningMarket = True ):
    
    #tickerData = get_ticker_stock(ticker,period,interval)
    #date = pd.Timestamp(time)

    
    """if date not in tickerData.index:
        return None"""
    print(time)
    try:
        if atOpeningMarket:
            price = tickerData.loc[str(time),"Open"]

        else:
            price = tickerData.loc[str(time), "Close"]
    except:
        print("non")
        return None
    
    return price
    

def get_last_available_price(tickerData, closingPrice = True ):
    if new_york_now < 16:
        price = tickerData["Close"].iloc[-2]
        print(f"price before closure yesterday : {price}")
    else:
        price =tickerData["Close"].iloc[-1]
        print(f"price before closure today : {price}")



    #tickerData = get_ticker_stock(ticker,period,interval)    
    """
    if closingPrice:
        price = tickerData["Close"].iloc[-2]

        if pd.isna(price):
            price = tickerData["Close"].iloc[-3]
    else:
        price = tickerData["Open"].iloc[-2]

        if pd.isna(price):
            price = tickerData["Open"].iloc[-3]
    """
    return price

    
