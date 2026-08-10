#3.12.10    
import yfinance as yf
from datetime import timedelta, datetime

from collections import defaultdict

import requests
import pandas as pd
from io import StringIO
import pytz # pour être sur la bourse américaine


now = datetime.today()
#print(now)
yesterday = (now - timedelta(days=1)).date() # le .date() permet de garder que l'année mois et jour

# make the code able to know if the bourse is open or close
new_york_now = datetime.now(pytz.timezone("America/New_York")).hour
#print(f"New york hours : {new_york_now}")

# aware and naive timezone
tz = pytz.timezone("America/New_York")
utc = pytz.UTC

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

    ticker_transaction = ticker_transaction.tz_localize(None)
    #print(info)
    tickerData = {
        "ticker":ticker,
        "data":ticker_transaction,
    }

    return tickerData

def get_purchase_history(return_with_price=False):

    all_purchase = defaultdict(list)

    with open("purchaseHistory.txt") as purchaseHistory:
        lines = purchaseHistory.readlines()

    fileLength = len(lines)

    if return_with_price:
        for i in range(fileLength):
            stockPurchase = lines[i].strip()        

            all_purchase[i].append(stockPurchase)
    
        all_purchase = dict(all_purchase)

        return all_purchase


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
    
    try:
        if atOpeningMarket:
            price = tickerData["data"].loc[str(time),"Open"]

        else:
            price = tickerData["data"].loc[str(time), "Close"]
    except:
        print("error in get_stock_price()")
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
    time = pd.Timestamp(time)

    openPrice = tickerData["data"].loc[time,"Open"]
    ticker_name = tickerData["ticker"]

    time = time.date()

    print(f"{time} - Purchase from {ticker_name} at {openPrice} $")

    with open("purchaseHistory.txt", "a") as purchaseHistory:
        # openPrice is for debug because the price will be check by Scalp.get_stock_price()
        purchaseHistory.write(f"{time} {ticker_name} {openPrice}\n") 
        return openPrice

def purchase_history_to_dataframe():
    print("I belive")

def compare_with_last_price(tickerData, time):
    last_price = get_last_available_price(tickerData)
    price = get_stock_price(time, tickerData)

    return last_price - price

def build_data_frame():
    columns = ["Ticker", "Date", "Date Price", "Current Price", "Variation"]

    ticker        = []
    date          = []
    price         = []
    current_price = []
    variation     = []

    all_purchase = get_purchase_history(True)

    for keys in all_purchase:
        print(keys)
        for values in all_purchase[keys]:
            print(values)

            values = values.split()


            date.append(values[0])
            ticker.append(values[1])
            price.append(values[2])




    #print(DataFrame)

build_data_frame()