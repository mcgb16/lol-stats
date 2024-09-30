from pymongo import MongoClient
import extras.ex_info as ex

client = MongoClient(ex.string_connection)

db_conn = client[ex.db]

itemsCollection = db_conn[ex.itemsCollection]
lolStatsCollection = db_conn[ex.lolStatsCollection]
runesCollection = db_conn[ex.runesCollection]
spellsCollection = db_conn[ex.spellsCollection]
championsCollection = db_conn[ex.championsCollection]