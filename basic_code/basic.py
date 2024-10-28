def calculate_time_seconds(sec_time):
    minutes = sec_time // 60
    seconds = sec_time % 60

    time_return = f"{minutes:02}:{seconds:02}"

    return time_return