#3.12.10    
import yfinance as yf
from datetime import timedelta, datetime

import random
import Scalp

now = datetime.today()
print(now)
yesterday = (now - timedelta(days=1)).date() # le .date() permet de garder que l'année mois et jour


period     = "max"
interval   = "1d"

purchaseTime1 = "2026-07-20"
purchaseTime2 = "2026-07-22"
purchaseTime3 = "2026-07-27"

"""
tickerData = Scalp.get_ticker_stock("AAPL")
allOpenPrice = tickerData[["Open"]].reset_index()
print(allOpenPrice)
allOpenPrice = tickerData[["Close"]].reset_index()
print(allOpenPrice)
"""



def purchase_open_stock(time,ticker):
    #print("purchase")

    tickerData = Scalp.get_ticker_stock(ticker, period, interval)
    #allOpenPrice = tickerData[["Open"]].reset_index()
    #print(allOpenPrice)
    openPrice = tickerData.loc[time,"Open"]

    print(f"{time} - Purchase from {ticker} at {openPrice} $")

    with open("purchaseHistory.txt", "a") as purchaseHistory:
        # openPrice is for debug because the price will be check by Scalp.get_stock_price()
        purchaseHistory.write(f"{time} {ticker} {openPrice}\n") 
        
def compare_2_last_price(time1, ticker):
    try:
        tickerData = Scalp.get_ticker_stock(ticker)

        price1 = Scalp.get_stock_price(time1, tickerData)
        last_price = Scalp.get_last_available_price(tickerData)

    except Exception as error :
        print(f"erreur : {error}")
        print(f"bourse probablement fermée")
        #exit()
        
    
    print(price1)
    print(last_price)

    difference = last_price - price1
    return difference


def check_all_purchase_history():
    all_purchase_history = Scalp.get_purchase_history()
    size_of_all_purchase_history = len(all_purchase_history)

    money = 0

    for keys in all_purchase_history:
        #print(keys)
        values = all_purchase_history[keys]
        #print(values)
        for items in values:
            #print(items)

            money = money + compare_2_last_price(items,keys)

    print(money)

