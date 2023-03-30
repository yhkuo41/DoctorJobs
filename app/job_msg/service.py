from datetime import datetime
from typing import List, Optional

import pymongo
from Levenshtein import ratio
from bson import ObjectId
from pymongo.collection import Collection

from app.job_msg.schema import JobMsgPutRequest, JobMsg, recent_ts, JobMsgQueryRequest, JobMsgDebugResponse
from app.job_msg.tagger.city_tagger import city_tagger
from app.job_msg.tagger.department_tagger import dept_tagger


async def tag_if_needed(job_msg: JobMsgPutRequest) -> None:
    if job_msg.auto_tag:
        job_msg.city_tags = city_tagger.tags_from_msg(job_msg.raw_msg)
        job_msg.dept_tags = dept_tagger.tags_from_msg(job_msg.raw_msg)
    if not job_msg.city_tags and not job_msg.dept_tags:
        raise ValueError("city_tags and dept_tags can not be both empty")


async def find_duplicate_job_msgs(job_msg: JobMsgPutRequest,
                                  db: Collection,
                                  levenshtein_ratio: float = 1.0) -> List[JobMsg]:
    query = {
        "is_delete": False,
        "_id": {"$gte": ObjectId.from_datetime(recent_ts())}
    }
    if job_msg.city_tags:
        query["city_tags"] = {"$in": [e.value for e in job_msg.city_tags]}
    if job_msg.dept_tags:
        query["dept_tags"] = {"$in": [e.value for e in job_msg.dept_tags]}

    query_res = db.find(filter=query, sort=[("_id", pymongo.DESCENDING)])
    res = []
    for m in query_res:
        raw_msg = m['raw_msg']
        # Exactly the same or the editing distance is above a certain point
        if levenshtein_ratio < 1.0 and ratio(job_msg.raw_msg, raw_msg) > levenshtein_ratio:
            res.append(JobMsg.from_mapping(m))
        elif raw_msg == job_msg.raw_msg:
            res.append(JobMsg.from_mapping(m))
    return res


async def update_job_msg(job_msg: JobMsgPutRequest, current_user_id: str, db: Collection) -> str:
    now = datetime.utcnow()
    db.update_one(
        {"_id": ObjectId(job_msg.job_msg_id)},
        {"$set": job_msg.to_update_mapping(now, current_user_id)}
    )
    return job_msg.job_msg_id


async def insert_job_msg(job_msg: JobMsgPutRequest, current_user_id: str, db: Collection) -> str:
    now = datetime.utcnow()
    res = db.insert_one(job_msg.to_insert_mapping(now, current_user_id))
    return str(res.inserted_id)


async def get_job_msg_by_id(job_msg_id: str, db: Collection) -> Optional[JobMsg]:
    res = db.find_one({"_id": ObjectId(job_msg_id), "is_delete": False})
    return JobMsg.from_mapping(res)


async def delete_job_msg_by_id(job_msg_id: str, current_user_id: str, db: Collection) -> bool:
    now = datetime.utcnow()
    res = db.update_one(
        {"_id": ObjectId(job_msg_id)},
        {"$set": JobMsgPutRequest.to_delete_mapping(now, current_user_id)}
    )
    return res.modified_count > 0


async def get_job_msgs(request: JobMsgQueryRequest, db: Collection) -> List[JobMsg]:
    query = {
        "_id": {"$gte": ObjectId.from_datetime(request.start_time)}
    }
    if request.end_time:
        query["end_time"] = {"$lte": request.end_time}
    if request.city_tags:
        query["city_tags"] = {"$in": [e.value for e in request.city_tags]}
    if request.dept_tags:
        query["dept_tags"] = {"$in": [e.value for e in request.dept_tags]}

    query_res = db.find(filter=query, sort=[("_id", pymongo.DESCENDING)], limit=request.limit, skip=request.skip)
    return [JobMsg.from_mapping(m) for m in query_res]


async def debug_job_msg(raw_msg: str) -> JobMsgDebugResponse:
    res = JobMsgDebugResponse(raw_msg=raw_msg)
    city_tagger.debug(res)
    dept_tagger.debug(res)
    return res
