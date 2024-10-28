import lol_infos.lol_apis as la
import lol_infos.lol_data_cleaning as ldc
import mongo_code.db_connection as db_conn

def ask_name_tag():
    player_name = input("Digite seu nick (sem a tag): ")
    player_tag = input("Digite sua tag: ")

    return player_name, player_tag

def connect_with_riot_api(name, tag):
    lol_acc = la.LolVerifier(name, tag)
    lol_acc_puuid = lol_acc.get_puuid()

    return lol_acc, lol_acc_puuid

def etl_matchs(lol_acc, puuid):
    all_matchs = lol_acc.get_all_matchs(puuid)

    print(len(all_matchs))

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
        match_data_cleaned.append(ldc.transforming_match_data(i))

    try:
        save_match_db = db_conn.create_match_db(match_data_cleaned)
    except Exception as e:
        save_match_db = f"Erro: {e}"

    return save_match_db

if __name__ == "__main__":
    pl_name, pl_tag = ask_name_tag()

    acc, acc_puuid = connect_with_riot_api(pl_name, pl_tag)

    match_db_result = etl_matchs(acc, acc_puuid)