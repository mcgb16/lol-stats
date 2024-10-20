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

def organize_match_timeline_data(match_dict):
    pass