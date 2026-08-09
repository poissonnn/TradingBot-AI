import streamlit as st

import matplotlib.pyplot as plt
from threading import RLock

import time 
import pandas as pd
import numpy as np

import Scalp
import Logic

from datetime import datetime, timedelta

now = datetime.today()
#print(now)
yesterday = (now - timedelta(days=1)).date() # le .date() permet de garder que l'année mois et jour



_lock = RLock()
#-----------------------------------------------
# VARIABLE FOR THE GRAPH

PRICE_WIDTH = 0.8
MEAN_WIDTH = 1.3
RAPPORT_WIDTH = 1.1
GRID_WIDTH = 0.6

Z_GRID = 0
Z_MEAN = 1
Z_PRICE = 3

red_dark    = [97 /255, 0  /255, 6  /255]
red_light   = [220/255, 100/255, 100/255]
orange_dark = [214/255, 40 /255, 40 /255]
orange      = [255/255, 127/255, 17 /255]
peach       = [255/255, 176/255, 144/255]
yellow      = [252/255, 191/255, 73 /255]

green_dark  = [91 /255, 126/255, 60 /255]
green_light = [100/255, 200/255, 100/255]

teal_dark   = [40 /255, 90 /255, 72 /255]
teal_medium = [64 /255, 138/255, 113/255]
teal_light  = [176/255, 228/255, 204/255]

blue_dark   = [56 /255, 82 /255, 180/255]
blue_light  = [100/255, 100/255, 220/255]

purple      = [93 /255, 28 /255, 106/255]
pink        = [202/255, 89 /255, 149/255]

black       = [50 /255, 51 /255, 57 /255]
true_black  = [0.1,0.1,0.1]
gray        = [150/255, 150/255, 150/255]
white       = [1, 1, 1]


#-----------------------------------------------
#PERSITANT DATA
if "date" not in st.session_state:
    st.session_state.date = yesterday

if "old_date" not in st.session_state:
    st.session_state.old_date = yesterday

if "last_price" not in st.session_state:
    st.session_state.last_price = 0.0

if "increment_clock" not in st.session_state:
    st.session_state.increment_clock = 0

if "rewind_time" not in st.session_state:
    st.session_state.rewind_time = False

if "time_sleep" not in st.session_state:
    st.session_state.time_sleep = 1.0

#if "tickerData" not in st.session_state:
#    st.session_state.tickerData = ""


#-----------------------------------------------
#SIDEBAR

with st.sidebar:
    st.session_state.date = st.date_input('Date')
    #print(st.session_state.date)
    #print(st.session_state.old_date)

    #make sure that changing date is not affected by : add_day
    if st.session_state and st.session_state.date != st.session_state.old_date:
        st.session_state.increment_clock = 0
        st.session_state.old_date = st.session_state.date
        print("différent")
        #print(st.session_state.date)
        #print(st.session_state.old_date)
        

    #increment a day
    add_day = st.button("add day")
    if add_day:
        st.session_state.increment_clock = st.session_state.increment_clock + 1
        print(st.session_state.increment_clock)

    st.session_state.rewind_time = st.toggle("Rewind time")

    st.session_state.time_sleep = st.select_slider("Chose time of each day", options=[
        0.001,
        0.1,
        0.3,
        0.5,
        0.75,
        1.0,
        1.5,
        2.0,
        5.0,]
    )
    # show current day
    header_date = st.session_state.date = st.session_state.date + timedelta(days=st.session_state.increment_clock)
    header_date = str(header_date)
    header_date = header_date.replace("-", " ")

    st.header(f"Date : {header_date}")

    # at the end to ensure that any prior input is taken in account before the rerun
    if st.session_state.rewind_time:
        st.session_state.increment_clock = st.session_state.increment_clock + 1
        print(st.session_state.increment_clock)
        time.sleep(st.session_state.time_sleep)

        st.rerun()

    show_graph = st.toggle("Show Graph")
#-----------------------------------------------
# ALGO INPUT





#-----------------------------------------------
# GRAPH
if show_graph:

    ticker_choice = st.text_input("Choose a ticker")

    periode_slider = st.select_slider("Chose periode",
        options=[
            "1d",
            "5d",
            "1mo",
            "3mo",
            "6mo",
            "1y",
            "2y",
            "5y",
            "10y",
            "ytd",
            "max",
        ],
        )
            
    if st.session_state.date and ticker_choice:
        
        tickerData = Scalp.get_ticker_stock(ticker_choice, periode_slider)
        #print(tickerData)
        print(st.session_state.date.strftime("%A"))
        
        #in week
        if st.session_state.date.strftime("%A") not in ("Saturday", "Sunday"):
            price = Scalp.get_stock_price(st.session_state.date, tickerData)

            #unexpected closure
            if price == None :
                print("Market close that day")
                st.subheader(f"Last {ticker_choice} price of a stock {round(st.session_state.last_price,3)}")
                st.caption("Market close")

            else:
                st.subheader(f"{ticker_choice} price of a stock {round(price,3)}")
                st.session_state.last_price = price

        # in weekend
        else:
            print("Market close for weekend")
            st.subheader(f"Last {ticker_choice} price of a stock {round(st.session_state.last_price,3)}")
            st.subheader("Market close for weekend")


        tickerDataGraph = tickerData["Close"]
        
        #print(tickerDataGraph)

        with _lock:
            ticker_data_graph_close = tickerData["Close"]
            ticker_data_graph_mean  = tickerData["Close"].mean()

            fig, axs = plt.subplots()
            axs.plot(tickerDataGraph,
                    color     = green_light,
                    linewidth = PRICE_WIDTH,
                    zorder    = Z_PRICE,
                    label     = ticker_choice )

            axs.axhline(ticker_data_graph_mean,
                    linewidth = MEAN_WIDTH ,
                    linestyle = (0,(2,2.5)),   
                    alpha     = 0.5,
                    label     = f"{ticker_choice} Mean",
                    color     = green_dark,
                    zorder    = Z_MEAN,)


            #axs.axvline(st.session_state.date,
            #        linewidth = MEAN_WIDTH ,
            #        linestyle = (0,(5,5)),   
            #        alpha     = 1,
            #        label     = f"{ticker_choice} Choose date",
            #        color     = teal_dark,
            #        zorder    = Z_MEAN,)

            axs.grid(True,
                    which     = "major",
                    alpha     = 0.25 ,
                    linestyle = "--",
                    linewidth = GRID_WIDTH,
                    color     = gray,
                    zorder    = Z_GRID)

            axs.legend(
                    loc       = "upper left",
                    frameon   = False,
                    fontsize  = 9,
                    labelcolor = black,
                    )   
            plt.tight_layout()
            st.pyplot(fig)


#purchase = st.button('purchase stock')

purchase = None

if purchase:
    if not ticker_choice:
        st.warning("Need a ticker")
        print("nonononon")

if purchase and ticker_choice:
    print(f"purchase {ticker_choice}")
    print(st.session_state.date)
    Logic.purchase_open_stock(str(st.session_state.date), ticker_choice)
    st.success(f"purchase stock from {ticker_choice} at {round(price, 3)}")
