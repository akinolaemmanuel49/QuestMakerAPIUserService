import pymongo
from pymongo.mongo_client import MongoClient

from core.config.env import Env

env = Env()


class UserDatabase:
    uri = 'mongodb+srv://' + env.MONGODB_USERNAME + ':' + \
        env.MONGODB_PASSWORD.get_secret_value() + \
        '@' + env.MONGODB_CLUSTER + '/?retryWrites=true&w=majority'
    client = MongoClient(uri)
    db = client['user_db']  # Set the database name to 'user_db'

    user_collection = db['user']  # Set the collection name to "user"
    # Create a unique constraint on the 'email' and 'auth_id' field in the 'user' collection
    user_collection.create_index(
        [('auth_id', pymongo.ASCENDING), ('email', pymongo.ASCENDING)], unique=True)
