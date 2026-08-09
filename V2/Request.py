#3.12.10    
import yfinance as yf
from datetime import timedelta, datetime

from collections import defaultdict

import requests
import pandas as pd
from io import StringIO
import pytz # pour être sur la bourse américaine


now = datetime.today()
print(now)
yesterday = (now - timedelta(days=1)).date() # le .date() permet de garder que l'année mois et jour

# make the code able to know if the bourse is open or close
new_york_now = datetime.now(pytz.timezone("America/New_York")).hour
print(f"New york hours : {new_york_now}")

# if the value for get_ticker_stock the period is "max" and the interval is "1d"
period     = "max"
interval   = "1d"

# debug variable
purchaseTime1 = "2026-07-20"
purchaseTime2 = "2026-07-24"
purchaseTime3 = "2026-08-07"


#get all the information about a ticker
def get_ticker_stock(ticker, period = "max", interval = "1d"):

    #print("hi from scalp")

    ticker_all_data = yf.Ticker(ticker)
    ticker_transaction = ticker_all_data.history(period=period, interval=interval)
    #print(info)
    tickerData = {
        "ticker":ticker,
        "data":ticker_transaction,
    }

    return tickerData

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
            price = tickerData["data"].loc[str(time),"Open"]

        else:
            price = tickerData["data"].loc[str(time), "Close"]
    except:
        print("non")
        return None
    
    return price
    
def get_last_available_price(tickerData, closingPrice = True ):
    if new_york_now < 16:
        price = tickerData["data"]["Close"].iloc[-2]
        print(f"price before closure yesterday : {price}")
    else:
        price =tickerData["data"]["Close"].iloc[-1]
        print(f"price before closure today : {price}")

    return price

def purchase_open_stock(time,tickerData):
    #print(allOpenPrice)
    openPrice = tickerData["data"].loc[time,"Open"]
    ticker_name = tickerData["ticker"]

    print(f"{time} - Purchase from {ticker_name} at {openPrice} $")

    with open("purchaseHistory.txt", "a") as purchaseHistory:
        # openPrice is for debug because the price will be check by Scalp.get_stock_price()
        purchaseHistory.write(f"{time} {ticker_name} {openPrice}\n") 
        return openPrice

tickerData = get_ticker_stock("AAPL","5d","1d")
print(tickerData["ticker"])
print(tickerData["data"])

