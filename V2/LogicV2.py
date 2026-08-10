#3.12.10

from datetime import timedelta, datetime
import Request
import Algorithme
# -------------------------------------------------------------------------------------------
# VARIABLE



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
start_date = "2025 07 11"
start_date = convert_str_to_datetime(start_date)

current_date = start_date

print(f"Simulation starting date : {start_date}")


print("\nChoose a ending date :")
#end_date = input()
end_date = "2025 07 20"
end_date = convert_str_to_datetime(end_date)
print(f"Simulation starting date : {end_date}")


simulation_periode = end_date - start_date
print(f"\nSimulation periode : {(simulation_periode).days} days")

print("\nChoose a starting budget (in usd) :")
#initial_budget = input()
initial_budget = 900
current_budget = initial_budget
print(f"Simulation starting with : {initial_budget} $")

# -------------------------------------------------------------------------------------------
#Simulation input
print("---------------------------")
print(f"\nCurrent date = {current_date}")

while current_date != end_date:

    #print(f"Current budget : {current_budget}")

    tickerData = Algorithme.choose_purchase(current_date)
    """
    if tickerData != None:
        stock_price = Request.get_stock_price(current_date,tickerData)
        if stock_price != None:
            if stock_price < current_budget:
                purchase_price = -stock_price

                print(purchase_price)
                print(current_budget)

            current_budget = current_budget + purchase_price
        else:
            print("No more money")
            break


    print(f"Current budget : {current_budget}")
    """
    # add time for next loop | NEED TO BE at the end
    print("# -------------------------")
    current_date = current_date + timedelta(days=1)

print(f"Current budget : {current_budget}")
print(f"\nCurrent date = {current_date}")
print("end")

