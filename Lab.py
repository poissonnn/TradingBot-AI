import yfinance as yf
from datetime import datetime, timedelta

import Scalp

period     = "1mo"
interval   = "1d"
userPeriod = 10
purchaseTime1 = "2026-07-22"
purchaseTime2 = "2026-07-23"

tickerData = Scalp.scan("AAPL", period, interval)
allOpenPrice = tickerData[["Open"]].reset_index()


print(allOpenPrice)