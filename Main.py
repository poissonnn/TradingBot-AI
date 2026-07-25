#3.12.10
import yfinance as yf
import datetime

now = datetime.date.today()
print(now)

import Scalp


period     = "5d"
interval   = "1d"
userPeriod = 10
purchaseTime1 = "2026-07-22"
purchaseTime2 = "2026-07-23"

tickerData = Scalp.scan("AAPL", period, interval)
allOpenPrice = tickerData[["Open"]].reset_index()
print(allOpenPrice)

def purchaseStock(time,ticker):
    #print("purchase")

    tickerData = Scalp.scan(ticker, period, interval)
    #allOpenPrice = tickerData[["Open"]].reset_index()
    #print(allOpenPrice)
    openPrice = tickerData.loc[time,"Open"]

    print(f"{time} - Purchase from {ticker} at {openPrice} $")

    with open("purchaseHistory.txt", "a") as purchaseHistory:
        purchaseHistory.write(f"{time} {ticker} {openPrice}\n")


purchaseStock(purchaseTime1,"AAPL")
purchaseStock(purchaseTime2,"AAPL")
