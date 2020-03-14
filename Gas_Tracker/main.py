from requests_html import HTMLSession
import datetime
import time
import util


def start_next_run_in_x_minutes(minutes: int):
    """
    pauses loop for x minutes
    :param minutes: I don't need to explain that, do I?
    """
    print("Next run starts in " + str(minutes) + " minutes.")
    print("Current time: " + str(datetime.datetime.today().time().strftime("%H:%M:%S")))
    print("=====")
    time.sleep(minutes * 60)


# Initializing some variables
page = "https://www.clever-tanken.de/tankstelle_details/45947"
today = datetime.datetime.today()
today = today.date()
data_logs_directory = "data_logs"
data_logs_path = "./" + data_logs_directory + "/" + str(today) + ".json"
last_update_search = ".price-footer"
update_string_search = "Preisänderung: "
loop_interval_time = 10  # minutes

print("Program starts...")
print("It's " + str(datetime.datetime.today().time().strftime("%H:%M:%S")))
print("=====")
while True:
    session = HTMLSession()
    response = session.get(page)

    if response:
        pass
    else:
        print("An error has occurred.")
        break

    gas_types = ["Diesel", "Super E10", "Super E5"]
    price_field = 0
    price_data_array = []
    for gas_type in gas_types:
        price_field += 1
        price_field_search = "#current-price-" + str(price_field)

        price = response.html.find(price_field_search)
        price = price[0].text

        last_update = response.html.find(last_update_search)
        last_update = last_update[0].text

        start_index = last_update.find(update_string_search) + len(update_string_search)
        end_index = start_index + 16
        last_update = last_update[start_index:end_index]

        last_update_date = datetime.datetime.strptime(last_update, "%d.%m.%Y %H:%M")
        last_update_date = last_update_date.strftime("%Y-%m-%d %H:%M")

        single_price_data = {
            'price': price
        }
        single_price_data = {gas_type: [single_price_data]}
        price_data_array.append(single_price_data)

    last_update = {
        "last_update": last_update_date
    }
    capture = [[price_data_array], last_update]

    price_data = {
        'captures': capture
    }

    util.check_and_create_dir(data_logs_directory)  # creates directory of data_logs
    if util.check_and_create_file_with_return(data_logs_path):  # creates json file in directory of data_logs
        data = util.load_data(data_logs_path)
        if data['captures'][1]['last_update'] == last_update_date:  # check if data is already logged
            print("Already logged!")
            start_next_run_in_x_minutes(loop_interval_time)
            continue

        for capture in data['captures']:
            price_data['captures'].append(capture)

    util.save_data(data_logs_path, price_data)
    print("New data has been saved to " + data_logs_path + "!")
    start_next_run_in_x_minutes(loop_interval_time)
