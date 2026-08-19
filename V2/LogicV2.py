#3.12.10

from datetime import timedelta, datetime
import Request
import Algorithme



# -------------------------------------------------------------------------------------------
# VARIABLE

now = datetime.today().date()
print(now)


# -------------------------------------------------------------------------------------------
def convert_str_to_datetime(date_str):
    format = "%y %m %d"
    datetime_str = datetime.strptime(date_str, "%Y %m %d").date()

    return datetime_str

# -------------------------------------------------------------------------------------------
#Simulation input

print("Choose a date in this format year month day")
print("\nChoose a starting date :")
#start_date = input()
start_date = "2026 01 01"
start_date = convert_str_to_datetime(start_date)

current_date = start_date

print(f"Simulation starting date : {start_date}")


print("\nChoose a ending date :")
#end_date = input()
end_date = "2026 01 15"
end_date = convert_str_to_datetime(end_date)
print(f"Simulation starting date : {end_date}")


simulation_periode = end_date - start_date
print(f"\nSimulation periode : {(simulation_periode).days} days")

print("\nChoose a starting budget (in usd) :")
#initial_budget = input()
initial_budget = 2800
current_budget = initial_budget
print(f"Simulation starting with : {initial_budget} $")

# -------------------------------------------------------------------------------------------
#Simulation input
print("---------------------------")
print(f"\nCurrent date = {current_date}")

#add purchased ticker and removed selled one
all_ticker_in_portfolio = []

#Simulation loop
while current_date != end_date:
    print(f"\n{current_date}")

    # only play when its not a week 
    if current_date.strftime("%A") not in ("Saturday", "Sunday"):

        #ask wich ticker to buy
        Simulation_action, ticker_name = Algorithme.choose_ticker(current_budget,all_ticker_in_portfolio)
        print(f"-- {Simulation_action}")

        # no action
        if Simulation_action == "Do_Nothing":
            current_date = current_date + timedelta(days=1)
            continue

        print(f"ticker name : {ticker_name}")
        tickerData = Request.get_ticker_stock(ticker_name)
        
        # get the stock price and check if the market is close or not
        stock_price = Request.get_stock_price(current_date, tickerData)

        #unexpected closure exit the loop
        if stock_price == None :
            print("Market close")

            current_date = current_date + timedelta(days=1)
            continue
            
        if Simulation_action == "Buy":
            #make the capital smaller by purchasing
            stock_price = -stock_price

            Request.update_purchase_history(current_date, tickerData, Simulation_action)

            all_ticker_in_portfolio.append(ticker_name)

        elif Simulation_action == "Sell":
            Request.update_purchase_history(current_date, tickerData, Simulation_action)

            all_ticker_in_portfolio.remove(ticker_name)


        
        # when a stock is purchase update the amount of money available
        #if tickerData != None:   

        purchase_price = stock_price

        print(purchase_price)
        print(current_budget)

      
        current_budget = current_budget + purchase_price
    # when is week do nothing and pass the day
    else:
        print("WEEKEND")

    # add time for next loop | NEED TO BE at the end
    current_date = current_date + timedelta(days=1)

#build dataframe | ONLY for debug
"""
dataFrame = Request.build_data_frame(end_date)

sum_stock_price, sum_current_stock_price, sum_stock_difference, variation = Request.calculate_other_data(dataFrame)


print(sum_stock_price)
print(sum_current_stock_price)
print(sum_stock_difference)
print(variation)
"""

dataFrame = Request.build_current_dataframe(now)

sum_stock_price, sum_current_stock_price, sum_stock_difference, variation = Request.calculate_other_data(dataFrame)


print(sum_stock_price)
print(sum_current_stock_price)
print(sum_stock_difference)
print(variation)
