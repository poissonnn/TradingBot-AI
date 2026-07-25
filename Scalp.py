import yfinance as yf

def scan(entreprise, period, interval):

    #print("hi from scalp")

    ticker = yf.Ticker(entreprise)
    info = ticker.history(period=period, interval=interval)
    #print(info)

    return info


