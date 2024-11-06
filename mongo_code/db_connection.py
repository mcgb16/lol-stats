from pymongo import MongoClient
import extras.ex_info as ex

client = MongoClient(ex.string_connection)

db_conn = client[ex.db]

items_collection = db_conn[ex.items_collection]
matchs_collection = db_conn[ex.matchs_collection]
runes_collection = db_conn[ex.runes_collection]
spells_collection = db_conn[ex.spells_collection]
champions_collection = db_conn[ex.champions_collection]
queues_collection = db_conn[ex.queues_collection]

def find_items(id_item):
    get_last_doc = [("_id", -1)]
    response = items_collection.find_one(sort=get_last_doc)

    try:
        if id_item == 0:
            return "None"
        else:
            id_item = str(id_item)
            get_item = response['data'][id_item]['name']

            return get_item
    except:
        return "No item found."

def find_runes(id_rune):
    id_rune = int(id_rune)
    search_rune = {
        "slots": {
            "$elemMatch": {
                "runes": {
                    "$elemMatch": {
                        "id": id_rune
                    }
                }
            }
        }
    }

    response = runes_collection.find_one(search_rune)
    try:
        for i in response['slots']:
            for k in i['runes']:
                if k['id'] == id_rune:
                    get_rune = k['name']
                    break

        return get_rune
    except:
        return "No rune find."

def find_summoner_spells(id_spell):
    get_last_doc = [("_id", -1)]

    response = spells_collection.find_one(sort=get_last_doc)

    spells_dict = response['data']

    for i in spells_dict.items():
        for k in i:
            if type(k) == dict:
                id_spell = str(id_spell)
                if k['key'] == id_spell:
                    get_spell = k['name']
                    break
    
    return get_spell

def find_champion_by_id(id_champion):
    get_last_doc = [("_id", -1)]

    response = champions_collection.find_one(sort=get_last_doc)

    champions_dict = response['data']

    for i in champions_dict.items():
        for k in i:
            if type(k) == dict:
                id_champion = str(id_champion)
                if k['key'] == id_champion:
                    get_champion = k['name']
                    break
    
    return get_champion

def find_champion_by_name(name_champion):
    get_last_doc = [("_id", -1)]

    response = champions_collection.find_one(sort=get_last_doc)

    champions_dict = response['data']

    for i in champions_dict.items():
        for k in i:
            if k == name_champion:
                get_champion = k
                break
    
    return get_champion

def find_match(id_match):
    search_match = {
        "match_id": id_match
    }

    response = matchs_collection.find_one(search_match)

    return response

def find_player_history(puuid):
    search_match_history = {
        "all_players" : {
            "$in" : [puuid]
        }
    }

    response = matchs_collection.find(search_match_history)

    match_history = []

    for i in response:
        match_history.append(i)

    return match_history

def create_match_db(matchs_data):
    try:
        save_result = matchs_collection.insert_many(matchs_data)
        
        return save_result
    except Exception as e:
        save_result = f"Erro: {e}"

        return save_result

def find_queue_type(queue_id):
    queue_id = int(queue_id)

    search_queue = {
        "queueId": queue_id
    }

    response = queues_collection.find_one(search_queue)

    queue_map = response["map"]
    queue_description = response["description"]

    queue_type = f"{queue_map} ({queue_description})"

    return queue_type


# print(find_items("7004"))
# print(find_runes("8008"))
# print(find_summoner_spells("7"))
# print(find_champion_by_id("22"))
# print(find_champion_by_name("Illaoi"))
# print(find_match("BR1_3004516580"))
# print(find_queue_type(440))