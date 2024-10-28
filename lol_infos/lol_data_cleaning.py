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
                champion_name = db_conn.find_champion_by_id(str(v))
                
                i[k] = champion_name
            else:
                continue
    
    for i in red_team_bans:
        for k,v in i.items():
            if k == "championId":
                if v == -1:
                    i[k] = "None"
                else:
                    champion_name = db_conn.find_champion_by_id(str(v))
                    
                    i[k] = champion_name
            else:
                continue

    teams_data["blue_team"]["bans"] = blue_team_bans
    teams_data["red_team"]["bans"] = red_team_bans
    
    return teams_data

def clean_players_data(players_data):
    for p in players_data:
        # Pegar o nome dos itens.
        p["item0"] = db_conn.find_items(str(p["item0"]))
        p["item1"] = db_conn.find_items(str(p["item1"]))
        p["item2"] = db_conn.find_items(str(p["item2"]))
        p["item3"] = db_conn.find_items(str(p["item3"]))
        p["item4"] = db_conn.find_items(str(p["item4"]))
        p["item5"] = db_conn.find_items(str(p["item5"]))
        p["item6"] = db_conn.find_items(str(p["item6"]))
        
        # Pegar o valor em minutos e segundos para as chaves de tempo.
        p["longestTimeSpentLiving"] = basic.calculate_time_seconds(p["longestTimeSpentLiving"])
        p["timePlayed"] = basic.calculate_time_seconds(p["timePlayed"])

        # Pegar o nome dos feitiços de invocador.
        p["summoner1Id"] = db_conn.find_summoner_spells(str(p["summoner1Id"]))
        p["summoner2Id"] = db_conn.find_summoner_spells(str(p["summoner2Id"]))

        # Ajustar as runas (perks).


def organize_match_timeline_data(match_dict):
    pass