from pymongo import MongoClient, collection, database
from os import getenv
from enum import Enum


class Collection(Enum):
    USERS = "users"
    TIME_LOGS = "time-logs"


class Controller:
    mongoClient: MongoClient = MongoClient(getenv("MONGO_CLIENT"))
    mongoDB: database.Database

    def __init__(self) -> None:
        self.mongoDB = self.mongoClient[getenv("MONGO_DB")]

    def collection(self, collection: Collection) -> collection.Collection:
        return self.mongoDB[collection.value]
