import lol_infos.lol_apis as la
import json

game_name = input("Digite seu nick (sem a tag): ")
game_tag = input("Digite sua tag: ")

lol_acc = la.LolVerifier(game_name, game_tag)

lol_acc_puuid = lol_acc.get_puuid()

all_matchs = lol_acc.get_all_matchs(lol_acc_puuid)

match_infos = lol_acc.get_match_geral_info(all_matchs[3])

with open("aaa.json", "a") as file:
    json.dump(match_infos, file, indent=4)