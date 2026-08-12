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
            
    except Exception as error:
        print(f"{error} in get_stock_price()")
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

    #print(f"{time} - Purchase from {ticker_name} at {openPrice} $")

    with open("purchaseHistory.txt", "a") as purchaseHistory:
        # openPrice is for debug because the price will be check by Scalp.get_stock_price()
        purchaseHistory.write(f"{time} {ticker_name} {openPrice}\n") 
        return openPrice

def compare_with_other_date(tickerData,stock_price ,date_to_compare):


    history_price = get_stock_price(date_to_compare,tickerData)

    while history_price == None:
        date_to_compare = date_to_compare - timedelta(days=1)
        history_price = get_stock_price(date_to_compare,tickerData)
        print("tkt si erreur")

    difference  = history_price - stock_price
    variation  = (history_price * 100) / stock_price-100

    return difference, variation, history_price

def compare_with_last_price(tickerData, stock_price):
    history_price = get_last_available_price(tickerData)

    difference  = history_price - stock_price
    variation  = (history_price * 100) / stock_price-100

    return difference, variation, history_price

def build_data_frame(Time_to_compare_to = True):
    print("I belive")

    all_ticker              = []
    all_date                = []
    all_stock_price         = []
    all_current_stock_price = []
    all_difference          = []
    all_variation           = []

    all_purchase = get_purchase_history(True)

    for keys in all_purchase:
        for values in all_purchase[keys]:
            # take the data from purchasehistory
            values = values.split()
            # 1 - Date
            all_date.append(values[0])

            #2 - Ticker
            ticker = values[1]
            all_ticker.append(ticker)

            #3 - Price at purchase
            history_stock_price = round(float(values[2]),2)
            all_stock_price.append(history_stock_price)

            #4-5-6
            #Difference between history and current price; the % and the current price
            #from the data of purchaseHistory i get other info
            tickerData = get_ticker_stock(ticker)

            if Time_to_compare_to == True:
                difference, variation, current_stock_price = compare_with_last_price(tickerData, history_stock_price)
            else:
                difference, variation, current_stock_price = compare_with_other_date(tickerData, history_stock_price,Time_to_compare_to)

            all_current_stock_price.append(round(current_stock_price, 2))
            all_difference.append(round(difference, 2))
            all_variation.append(round(variation, 2))

    if Time_to_compare_to == True:
        columns = ["Ticker", "Date", "Price", f"Price from {now.date()}", "Difference", "Variation"]
    else:
        columns = ["Ticker", "Date", "Price", f"Price from {Time_to_compare_to}", "Difference", "Variation"]

    DataFrame = pd.DataFrame(list(zip(all_ticker, all_date, all_stock_price, all_current_stock_price, all_difference, all_variation)),
                    columns = columns )

    return DataFrame

def calculate_other_data(dataFrame):
    print(dataFrame)

    round_number = 3

    sum_stock_price         = round(dataFrame["Price"].sum(), round_number)
    sum_current_stock_price = round(dataFrame[dataFrame.columns[3]].sum(), round_number)
    sum_stock_difference    = round(sum_current_stock_price - sum_stock_price, round_number)
    # (VA - VD / VD )* 100
    variation = round((((sum_current_stock_price - sum_stock_price )/ sum_stock_price) * 100), round_number)


    """
    # C'est une oeuvre d'art mais c'est aussi inutile
    # Work of art but useless

    columns = [ "Price", dataFrame.columns[3], "Difference", "Variation"]
    columns_data = [sum_stock_price, sum_current_stock_price, sum_stock_difference, sum_stock_variation]

    print(columns_data[1])
    columns_data[1] = columns_data[1] +1 
    print(columns_data[1])

    for i in range(len(columns)):
        print(columns[i])

        for value in dataFrame[columns[i]]:
            columns_data[i] = columns_data[i] + value
        
        print(columns_data[i]) 
    """



    return sum_stock_price, sum_current_stock_price, sum_stock_difference, variation


df_debug = pd.DataFrame([
    ["TPR",  "2025-01-02", 64.22, 68.68, 4.46, 6.95],
    ["FITB", "2025-01-03", 40.24, 41.37, 1.13, 2.80],
    ["GNRC", "2025-01-06", 160.98, 161.86, 0.88, 0.55],
    ["GOOG", "2025-01-07", 197.24, 197.02, -0.22, -0.11],
    ["CRH",  "2025-01-08", 90.64, 95.93, 5.29, 5.84],
    ["IQV",  "2025-01-10", 202.71, 198.42, -4.29, -2.12],
    ["VZ",   "2025-01-13", 34.40, 34.83, 0.43, 1.25],
    ["RCL",  "2025-01-14", 224.37, 230.20, 5.83, 2.60],
    ["SYK",  "2025-01-15", 359.26, 379.43, 20.17, 5.61],
    ["DOV",  "2025-01-16", 187.99, 192.72, 4.73, 2.52],
], columns=[
    "Ticker",
    "Date",
    "Price",
    "Price from 2025-01-17",
    "Difference",
    "Variation"
])

"""
df_debug["Date"] = pd.to_datetime(df_debug["Date"])

calculate_other_data(df_debug)
"""