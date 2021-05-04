import key
import pymongo


class MongoDB(object):
    def __init__(self, client="tenet", db="tenet_db"):
        self.__client = pymongo.MongoClient(key._mongo_uri)
        __db = self.__client[client]
        self.__col = __db[db]

    def _insert(self, obj, checkIfexists=False):
        if checkIfexists == True:
            return self.__col.save(obj)
        self.__col.insert_one(obj)

    def _update(self, where_condition, set_data):
        self.__col.update_one(where_condition, set_data)

    def _find(self, obj=None, _limit=0, _offset=0):
        return self.__col.find(obj).skip(_offset).limit(_limit)

    def _sorted_find(self, obj=None, _limit=0, _sort=None, _offset=0):
        if _sort == None:
            _sort = -1
        return self.__col.find(obj).skip(_offset).limit(_limit).sort("_id", _sort)

    def __del__(self):
        self.__client.close()
        print("DB Closed!!")
