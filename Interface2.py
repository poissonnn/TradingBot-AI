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

#-----------------------------------------------
#SIDEBAR -> simulation input :
# start + end date ; initial budget ; (algorythme name) ; start button

with st.sidebar:
    st.header("Simulation data and input")
    start_date = st.date_input("Starting date")
    end_date = st.date_input("Ending date")

    initial_budget = st.number_input("Choose initial budget")


    start_date_str = str(start_date).replace("-", " ")  
    st.header(f"Start at : {start_date_str}")

    end_date_str = str(end_date).replace("-", " ")
    st.header(f"End at : {end_date_str}")   

    simulation_periode = end_date-start_date
    st.header(f"Simulation periode : {(simulation_periode).days} days")

    st.header(f"With an initial budget of {initial_budget} $")

    print(start_date)
    print(end_date)

    

    print(simulation_periode)

    now = datetime.today()

    yesterday = (now - timedelta(days=1)).date()


    start_simulation = st.button("Start the Simulation")

    min_simulation_periode = 10
    min_initial_budget = 50

    if simulation_periode < min_simulation_periode:
        st.warning(f"Simulation periode need to be more than {min_simulation_periode} days")

    elif initial_budget < min_initial_budget:
        st.warning(f"Initial budget need to be over {min_initial_budget} $")

    elif start_simulation :
        st.success(f"Simulation started")


