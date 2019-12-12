from os import getenv
from flask_pymongo import PyMongo

mongo = None


class mongoData:
    def __init__(self, app):
        self.app = app

    def __get_mongo(self):
        global mongo

        if 'MONGO_URI' not in self.app.config:
            mongo_password = getenv("MONGO_PASSWORD", "")
            self.app.config["MONGO_URI"] = "mongodb+srv://admin:{}@cluster0-hb5he.mongodb.net/artist_service?retryWrites=true&w=majority".format(mongo_password)

        if not mongo:
            mongo = PyMongo(self.app)

        return mongo

    def filter(self, object):
        return self.__get_mongo().db.artists.find(object)

    def get_all(self):
        return self.__get_mongo().db.artists.find({})

    def add_one(self, data):
        return self.__get_mongo().db.artists.insert_one(data)

    def add_many(self, objects):
        return self.__get_mongo().db.artists.insert_many(objects)

    def get_one(self, object):
        return self.__get_mongo().db.artists.find_one(object)


