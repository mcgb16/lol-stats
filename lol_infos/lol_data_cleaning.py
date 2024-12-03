import mongo_code.db_connection as db_conn
import basic_code.basic as basic

def organize_match_geral_data(match_dict):
    players_info_list = match_dict['info']['participants']

    info_to_exclude = [
        "allInPings",
        "assistMePings",
        "basicPings",
        "bountyLevel",
        "challenges",
        "champExperience",
        "championTransform",
        "commandPings",
        "consumablesPurchased",
        "damageDealtToBuildings",
        "dangerPings",
        "eligibleForProgression",
        "enemyMissingPings",
        "enemyVisionPings",
        "getBackPings",
        "holdPings",
        "individualPosition",
        "itemsPurchased",
        "lane",
        "largestCriticalStrike",
        "missions",
        "needVisionPings",
        "nexusKills",
        "nexusLost",
        "nexusTakedowns",
        "objectivesStolenAssists",
        "onMyWayPings",
        "participantId",
        "placement",
        "playerAugment1",
        "playerAugment2",
        "playerAugment3",
        "playerAugment4",
        "playerAugment5",
        "playerAugment6",
        "playerSubteamId",
        "pushPings",
        "role",
        "sightWardsBoughtInGame",
        "subteamPlacement",
        "summonerName",
        "visionClearedPings"
    ]

    for i in range (len(players_info_list)):
        for k in info_to_exclude:
            if k in players_info_list[i]:
                del players_info_list[i][k]
        
        players_info_list[i]["dpmChampions"] = ((players_info_list[i]["physicalDamageDealtToChampions"] + players_info_list[i]["magicDamageDealtToChampions"]) / match_dict['info']['gameDuration']) * 60
        players_info_list[i]["dpmTurrets"] = (players_info_list[i]["damageDealtToTurrets"] / match_dict['info']['gameDuration']) * 60
        players_info_list[i]["dpmTotal"] = ((players_info_list[i]["physicalDamageDealt"] + players_info_list[i]["magicDamageDealt"]) / match_dict['info']['gameDuration']) * 60
        players_info_list[i]["fpm"] = ((players_info_list[i]["totalMinionsKilled"] + players_info_list[i]["totalAllyJungleMinionsKilled"] + players_info_list[i]["totalEnemyJungleMinionsKilled"]) / match_dict['info']['gameDuration']) * 60
        players_info_list[i]["vspm"] = (players_info_list[i]["visionScore"] / match_dict['info']['gameDuration']) * 60
        players_info_list[i]["gpm"] = (players_info_list[i]["goldEarned"] / match_dict['info']['gameDuration']) * 60

        
        try:
            players_info_list[i]["kda"] = ((players_info_list[i]["kills"] + players_info_list[i]["assists"]) / players_info_list[i]["deaths"])
        except:
            players_info_list[i]["kda"] = (players_info_list[i]["kills"] + players_info_list[i]["assists"])
        
        players_info_list[i]["goldEfficiency"] = ((players_info_list[i]["physicalDamageDealtToChampions"] + players_info_list[i]["magicDamageDealtToChampions"] + players_info_list[i]["damageDealtToTurrets"]) / players_info_list[i]["goldEarned"])
        
        if players_info_list[i]["teamId"] == match_dict['info']['teams'][0]["teamId"]:
            try:
                players_info_list[i]["kp"] = ((players_info_list[i]["kills"] + players_info_list[i]["assists"]) / match_dict['info']['teams'][0]["objectives"]["champion"]["kills"]) * 100
            except:
                players_info_list[i]["kp"] = 0
        else:
            try:
                players_info_list[i]["kp"] = ((players_info_list[i]["kills"] + players_info_list[i]["assists"]) / match_dict['info']['teams'][1]["objectives"]["champion"]["kills"]) * 100
            except:
                players_info_list[i]["kp"] = 0
    
    match_data = {
        'match_id': match_dict['metadata']['matchId'],
        'all_players': match_dict['metadata']['participants'],
        'game_data': {
            'game_duration': match_dict['info']['gameDuration'], 
            'queue_id': match_dict['info']['queueId'], 
            'game_mode': match_dict['info']['gameMode'], 
            'game_id': match_dict['info']['gameId'],
            'game_creation_time': match_dict['info']['gameCreation'],
            'game_version': match_dict['info']['gameVersion'],
            'region': match_dict['info']['platformId']
        },
        'teams_data': {
            'blue_team': match_dict['info']['teams'][0],
            'red_team': match_dict['info']['teams'][1]
        },
        'players_data': players_info_list
    }

    return match_data

def clean_teams_data(teams_data):
    blue_team_bans = teams_data["blue_team"]["bans"]
    red_team_bans = teams_data["red_team"]["bans"]

    for i in blue_team_bans:
        for k,v in i.items():
            if k == "championId":
                if v == -1:
                    i[k] = "None"
                else:
                    champion_name = db_conn.find_champion_by_id(v)
                    
                    i[k] = champion_name
            else:
                continue
    
    for i in red_team_bans:
        for k,v in i.items():
            if k == "championId":
                if v == -1:
                    i[k] = "None"
                else:
                    champion_name = db_conn.find_champion_by_id(v)
                    
                    i[k] = champion_name
            else:
                continue

    teams_data["blue_team"]["bans"] = blue_team_bans
    teams_data["red_team"]["bans"] = red_team_bans
    
    return teams_data

def clean_players_data(players_data):
    for p in players_data:
      # Pegar o nome dos itens.

      p["item0"] = db_conn.find_items(p["item0"])
      p["item1"] = db_conn.find_items(p["item1"])
      p["item2"] = db_conn.find_items(p["item2"])
      p["item3"] = db_conn.find_items(p["item3"])
      p["item4"] = db_conn.find_items(p["item4"])
      p["item5"] = db_conn.find_items(p["item5"])
      p["item6"] = db_conn.find_items(p["item6"])
      
      # Pegar o valor em minutos e segundos para as chaves de tempo.
      p["longestTimeSpentLiving"] = basic.calculate_time_seconds(p["longestTimeSpentLiving"])
      p["timePlayed"] = basic.calculate_time_seconds(p["timePlayed"])

      # Pegar o nome dos feitiços de invocador.
      p["summoner1Id"] = db_conn.find_summoner_spells(p["summoner1Id"])
      p["summoner2Id"] = db_conn.find_summoner_spells(p["summoner2Id"])

      # Ajustar as runas principais (perks).
      p["primaryRuneMain"] = db_conn.find_runes(p["perks"]["styles"][0]["selections"][0]["perk"])
      p["primaryRune1"] = db_conn.find_runes(p["perks"]["styles"][0]["selections"][1]["perk"])
      p["primaryRune2"] = db_conn.find_runes(p["perks"]["styles"][0]["selections"][2]["perk"])
      p["primaryRune3"] = db_conn.find_runes(p["perks"]["styles"][0]["selections"][3]["perk"])

      # Ajustar as runas secundárias (perks).
      p["secundaryRune1"] = db_conn.find_runes(p["perks"]["styles"][1]["selections"][0]["perk"])
      p["secundaryRune2"] = db_conn.find_runes(p["perks"]["styles"][1]["selections"][1]["perk"])

      del p["perks"]

    return players_data

def clean_game_data(game_data):
    game_data["queue_id"] = db_conn.find_queue_type(game_data["queue_id"])
    game_data["game_duration"] = basic.calculate_time_seconds(game_data["game_duration"])
    game_data["game_creation_time"] = basic.calculate_timestamps(game_data["game_creation_time"])

    game_data["game_end_time"] = basic.sum_data(game_data["game_creation_time"], game_data["game_duration"])

    return game_data

def clean_elo_data(lol_acc, acc_sum_id):
    pl_elos = lol_acc.get_acc_ranks(acc_sum_id)

    pl_elos_cleaned = []
    pl_elo_index = {
        "Queue" : "",
        "Tier" : "",
        "Rank" : "",
        "Lp" : "",
        "Wins" : "",
        "Losses" : ""
    }

    for i in pl_elos:
        pl_elo_index["Queue"] = i["queueType"]
        pl_elo_index["Tier"] = i["tier"]
        pl_elo_index["Rank"] = i["rank"]
        pl_elo_index["Lp"] = i["leaguePoints"]
        pl_elo_index["Wins"] = i["wins"]
        pl_elo_index["Losses"] = i["losses"]
        pl_elos_cleaned.append(pl_elo_index.copy())
    
    return pl_elos_cleaned

def organize_match_timeline_data(match_dict):
    pass

