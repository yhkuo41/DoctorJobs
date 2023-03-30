from datetime import datetime
from typing import Optional

from bson import ObjectId
from pymongo.collection import Collection

from app.user.hashing import get_password_hash
from app.user.schema import UserBase, User


async def verify_exist(user: UserBase, db: Collection) -> bool:
    return db.count_documents({"$or": [{"account": user.account}, {"email": user.email}]}, limit=1) > 0


async def new_user_register(user: UserBase, db: Collection) -> str:
    hashed = get_password_hash(user.password.get_secret_value())
    now = datetime.utcnow()
    res = db.insert_one({
        "account": user.account,
        "password": hashed,
        "email": user.email,
        "line_user_id": user.line_user_id,
        "name": user.name,
        "update_ts": now,
        "is_delete": False
    })
    return str(res.inserted_id)


async def get_user_by_user_id(user_id: str, db: Collection) -> Optional[User]:
    res = db.find_one({"_id": ObjectId(user_id), "is_delete": False})
    return User.from_mapping(res)


def get_user_by_account(account: str, db: Collection) -> Optional[User]:
    res = db.find_one({"account": account, "is_delete": False})
    return User.from_mapping(res)
