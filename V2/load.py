import Request


from datetime import timedelta, datetime

now = datetime.today().date()
print(now)

def convert_str_to_datetime(date_str):
    format = "%y %m %d"
    datetime_str = datetime.strptime(date_str, "%Y %m %d").date()

    return datetime_str

print(f"Start a simulation[1] of make a dataframe[2] :")

choice = input().strip()
choice = int(choice)

if choice == 1:
    import LogicV2

elif choice == 2:

    """
    start_date = "2026 04 01"
    start_date = convert_str_to_datetime(start_date)

    end_date = "2026 05 01"
    end_date = convert_str_to_datetime(end_date)


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
