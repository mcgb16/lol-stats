import lol_infos.lol_apis as la
import lol_infos.lol_data_cleaning as ldc
import json

game_name = input("Digite seu nick (sem a tag): ")
game_tag = input("Digite sua tag: ")

lol_acc = la.LolVerifier(game_name, game_tag)

lol_acc_puuid = lol_acc.get_puuid()

all_matchs = lol_acc.get_all_matchs(lol_acc_puuid)

match_infos = lol_acc.get_match_geral_info(all_matchs[3])

match_metadata, match_relevant_data, match_players_data, match_teams_data = ldc.organize_match_data(match_infos)