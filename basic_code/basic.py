from datetime import date, datetime, timedelta

def calculate_time_seconds(sec_time):
    sec_time = int(sec_time)
    minutes = sec_time // 60
    seconds = sec_time % 60

    time_return = f"{minutes:02}:{seconds:02}"

    return time_return

def calculate_timestamps(timestamp_milliseconds):
    timestamp_milliseconds = int(timestamp_milliseconds)

    timestamp_seconds = timestamp_milliseconds / 1000

    timestamp_date = datetime.fromtimestamp(timestamp_seconds)

    formatted_timestamp_date = timestamp_date.strftime("%d-%m-%Y %H:%M:%S")

    return formatted_timestamp_date

def sum_data(initial_data, sum_time):
    initial_data_adjusted = datetime.strptime(initial_data, "%d-%m-%Y %H:%M:%S")

    sum_time_minutes, sum_time_seconds = sum_time.split(":")

    sum_time_adjusted = timedelta(minutes=int(sum_time_minutes), seconds=int(sum_time_seconds))

    final_data = initial_data_adjusted + sum_time_adjusted

    formatted_final_data = final_data.strftime("%d-%m-%Y %H:%M:%S")

    return formatted_final_data