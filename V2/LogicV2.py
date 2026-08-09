#3.12.10

from datetime import timedelta, datetime
import Request
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
start_date = "2026 07 01"
start_date = convert_str_to_datetime(start_date)

current_date = start_date

print(f"Simulation starting date : {start_date}")


print("\nChoose a ending date :")
#end_date = input()
end_date = "2026 08 01"
end_date = convert_str_to_datetime(end_date)
print(f"Simulation starting date : {end_date}")


simulation_periode = end_date - start_date
print(f"\nSimulation periode : {(simulation_periode).days} days")

print("\nChoose a starting budget (in usd) :")
#initial_budget = input()
initial_budget = 5000
print(f"Simulation starting with : {initial_budget} $")

# -------------------------------------------------------------------------------------------
#Simulation input
print("---------------------------")
print(f"\nCurrent date = {current_date}")

while current_date != end_date:

    print(f"Current date = {current_date}")

    


    current_date = current_date + timedelta(days=1)


print(f"\nCurrent date = {current_date}")
print("end")