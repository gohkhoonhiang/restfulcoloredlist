from pymongo import MongoClient
from tornado.options import options


def create_db():
    client = MongoClient(options.dbhost, options.dbport)
    db = client[options.dbname]
    return db
    
db = create_db()


