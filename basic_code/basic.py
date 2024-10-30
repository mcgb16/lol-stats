from datetime import datetime, timedelta
import lol_infos.lol_data_cleaning as ldc
import mongo_code.db_connection as db_conn

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

def ask_name_tag():
    player_name = input("Digite seu nick (sem a tag): ")
    player_tag = input("Digite sua tag: ")

    return player_name, player_tag

def save_player_history(lol_acc, lol_acc_puuid):
    all_matchs = lol_acc.get_all_matchs(lol_acc_puuid)

    match_infos = []

    for i in all_matchs:
        match_exists_db = db_conn.find_match(i)
        if match_exists_db == None:
            match_infos.append(lol_acc.get_match_geral_info(i))
        else:
            continue

    match_data_organized = []

    for i in match_infos:
        match_data_organized.append(ldc.organize_match_geral_data(i))

    match_data_cleaned = []

    for i in match_data_organized:
        i["teams_data"] = ldc.clean_teams_data(i["teams_data"])
        i["game_data"] = ldc.clean_game_data(i["game_data"])
        i["players_data"] = ldc.clean_players_data(i["players_data"])

        match_data_cleaned.append(i)
        
    save_match_db = db_conn.create_match_db(match_data_cleaned)

    return save_match_db