import streamlit as st
import pandas as pd

import Scalp


date = st.date_input('Date')

purchase = st.button('purchase stock')

ticker_choice = st.text_input("Choose a ticker")

tickerData = Scalp.get_ticker_stock(str(ticker_choice))
price = Scalp.get_stock_price(str(date),tickerData)
st.subheader(f"{ticker_choice} price of a stock {price}")