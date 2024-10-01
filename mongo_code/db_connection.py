from pymongo import MongoClient
import extras.ex_info as ex

client = MongoClient(ex.string_connection)

db_conn = client[ex.db]

itemsCollection = db_conn[ex.itemsCollection]
lolStatsCollection = db_conn[ex.lolStatsCollection]
runesCollection = db_conn[ex.runesCollection]
spellsCollection = db_conn[ex.spellsCollection]
championsCollection = db_conn[ex.championsCollection]

def find_items(id_item):
    get_last_doc = [("_id", -1)]
    response = itemsCollection.find_one(sort=get_last_doc)

    get_item = response['data'][id_item]['name']

    return get_item

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

    response = runesCollection.find_one(search_rune)

    for i in response['slots']:
        for k in i['runes']:
            if k['id'] == id_rune:
                get_rune = k['name']
                break

    return get_rune


print(find_items("3153"))
print(find_runes("8008"))
