import logging

import pymongo

from app import config

mongo_client = pymongo.MongoClient(config.get_secret("MONGO_CONN_STR"), tz_aware=True)
db_name = config.get_secret("MONGO_DB_NAME")
logger = logging.getLogger()
logger.info("Using MongoDB %s", db_name)


def get_db():
    db = mongo_client[db_name]
    yield db
