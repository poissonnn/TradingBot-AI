#3.12.10
import yfinance as yf
from datetime import timedelta, datetime

import random
import Scalp

now = datetime.today()
print(now)
yesterday = (now - timedelta(days=1)).date() # le .date() permet de garder que l'année mois et jour
print(yesterday)

period     = "5d"
interval   = "1d"
userPeriod = 10
purchaseTime1 = "2026-07-24"
purchaseTime2 = "2026-07-28"

tickerData = Scalp.get_tinker_stock("AAPL", period, interval)
allOpenPrice = tickerData[["Open"]].reset_index()
print(allOpenPrice)
allOpenPrice = tickerData[["Close"]].reset_index()
print(allOpenPrice)


def purchase_stock(time,ticker):
    #print("purchase")

    tickerData = Scalp.get_tinker_stock(ticker, period, interval)
    #allOpenPrice = tickerData[["Open"]].reset_index()
    #print(allOpenPrice)
    openPrice = tickerData.loc[time,"Open"]

    print(f"{time} - Purchase from {ticker} at {openPrice} $")

    with open("purchaseHistory.txt", "a") as purchaseHistory:
        purchaseHistory.write(f"{time} {ticker} {openPrice}\n")

#purchase_stock(purchaseTime1,"OKE")

def check_stock_price(time,ticker,isOpen = True):
    tickerData = Scalp.get_tinker_stock(ticker, period, interval)
    if isOpen:
        price = tickerData.loc[str(time),"Open"]
    else:
        price = tickerData.loc[str(time), "Close"]
    return price


def get_purchase_history():

    with open("purchaseHistory.txt") as purchaseHistory:
        lines = purchaseHistory.readlines()
    print(lines)
    fileLength = len(lines)
    print(fileLength)

    for i in range(fileLength):
        #take the line
        stockPurchase = lines[i].strip()
        stockPurchase = stockPurchase.split() # split each element separated by a space

        print(stockPurchase)
        """
        # extract the date(0); the ticker(1); price(2)
        date = stockPurchase[0]
        date = date.strip()
        print(date)

        ticker = stockPurchase[1]
        ticker = ticker.strip()
        print(ticker)

        price = stockPurchase[2]
        price = price.strip()
        price = float(price)
        """
            

def compare_2_stock(time1,time2, ticker):
    try:
        price1 = check_stock_price(time1, ticker)
        price2 = check_stock_price(time2, ticker, False)
    except Exception as error :
        print(f"erreur : {error}")
        print(f"bourse probablement fermée")
        #exit()
        
    
    print(price1)
    print(price2)

    difference = price2 - price1
    print(difference)

    
#check_stock_price(yesterday,"AAPL", False)
#compare_stock(purchaseTime1,yesterday,"AAPL")

