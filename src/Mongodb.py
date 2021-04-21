import key
import pymongo


class MongoDB(object):
    def __init__(self, client="tenet", db="tenet_db"):
        self.__client = pymongo.MongoClient(key._mongo_uri)
        __db = self.__client[client]
        self.__col = __db[db]

    def _insert(self, obj):
        self.__col.insert_one(obj)

    def _update(self, where_condition, set_data):
        self.__col.update_one(where_condition, set_data)

    def _find(self):
        return self.__col.find().sort({ _id: -1 })

    def __del__(self):
        self.__client.close()
        print("DB Closed!!")
