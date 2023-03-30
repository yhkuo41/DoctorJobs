import logging
from typing import Any

import pymongo

from app import config


def require_not_none(obj: Any):
    if obj is not None:
        return obj
    raise ValueError


mongo_client = pymongo.MongoClient(config.get_secret("MONGO_CONN_STR"))
db_name = config.get_secret("MONGO_DB_NAME")
logging.info(f"using mongodb {db_name}")
db = require_not_none(mongo_client[db_name])

user_col = require_not_none(db["user"])
job_msg_col = require_not_none(db["job_msg"])
