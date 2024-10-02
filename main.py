import lol_infos.lol_apis as la
import lol_infos.lol_data_cleaning as ldc
import mongo_code.db_connection as dbc
import json

game_name = input("Digite seu nick (sem a tag): ")
game_tag = input("Digite sua tag: ")

lol_acc = la.LolVerifier(game_name, game_tag)

lol_acc_puuid = lol_acc.get_puuid()

all_matchs = lol_acc.get_all_matchs(lol_acc_puuid)

match_infos = []

for i in all_matchs:
    match_infos.append(lol_acc.get_match_geral_info(i))

match_data_cleaned = []

for i in match_infos:
    match_data_cleaned.append(ldc.organize_match_data(i))

post_match = dbc.create_match_db(match_data_cleaned)