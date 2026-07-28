#3.12.10
import yfinance as yf
import datetime

import random
import Scalp

now = datetime.date.today()
print(now)

period     = "5d"
interval   = "1d"
userPeriod = 10
purchaseTime1 = "2026-07-22"
purchaseTime2 = "2026-07-23"

#tickerData = Scalp.get_tinker_stock("AAPL", period, interval)
#allOpenPrice = tickerData[["Open"]].reset_index()
#print(allOpenPrice)

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

with open("purchaseHistory.txt") as purchaseHistory:
    lines = purchaseHistory.readlines()

print(lines)
