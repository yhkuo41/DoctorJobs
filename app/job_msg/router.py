from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import constr, confloat
from pymongo.database import Database

from app.auth.jwt import CurrentUserDep
from app.db import database
from app.job_msg import service
from app.job_msg.schema import JobMsgPutRequest, JobMsgIdResponse, JobMsg, QUERY_TIME_LIMIT, JobMsgQueryRequest, \
    JobMsgDebugResponse

job_msg_router = APIRouter(tags=["Job Message"], prefix="/job_msg")


@job_msg_router.put("/")
async def create_or_update_job_msg(job_msg: JobMsgPutRequest,
                                   current_user: CurrentUserDep,
                                   db: Database = Depends(database.get_db)) -> JobMsgIdResponse:
    """新增或更新job_msg</br>
    自動或手動標籤後，若city_tags和dept_tags都為空，則會拋出例外，之後會根據標籤撈取近期訊息，並判斷完全相同的訊息
    為重複，若無重複訊息，則直接新增，若重複的訊息只有一筆，則直接更新，否則拋出例外</br>

    Returns: 新增或更新的job_msg_id
    """
    await service.tag_if_needed(job_msg)
    duplicates = await service.find_duplicate_job_msgs(job_msg, db.job_msg)
    if len(duplicates) > 1:
        raise HTTPException(
            status_code=409,
            detail=f"Found more than one identical job_msg with the same message in the last {QUERY_TIME_LIMIT.days} "
                   f"days of data, duplicate msg ids: {[m.job_msg_id for m in duplicates]}. Please delete duplicate "
                   f"job_msg"
        )
    if len(duplicates) == 1:  # update
        if job_msg.job_msg_id and job_msg.job_msg_id != duplicates[0].job_msg_id:
            raise HTTPException(
                status_code=409,
                detail=f"Find a duplicate job_msg whose job_msg_id is '{duplicates[0].job_msg_id}', "
                       f"and the job_msg_id to be updated is different from it"
            )
        job_msg.job_msg_id = duplicates[0].job_msg_id
        job_msg_id = await service.update_job_msg(job_msg, current_user.user_id, db.job_msg)
    else:
        job_msg_id = await service.insert_job_msg(job_msg, current_user.user_id, db.job_msg)
    return JobMsgIdResponse(job_msg_id=job_msg_id)


@job_msg_router.get("/duplicates")
async def get_duplicate_job_msgs(raw_msg: constr(min_length=20, max_length=2000, strip_whitespace=True),
                                 current_user: CurrentUserDep,
                                 db: Database = Depends(database.get_db),
                                 levenshtein_ratio: confloat(ge=0, le=1) = 1.0) -> list[JobMsg]:
    """將原始訊息自動打上標籤後，以標籤搜尋近似的訊息，並以編輯距離判斷是否重複

    Args:</br>
        raw_msg (): 原始訊息</br>
        levenshtein_ratio (): 編輯距離比門檻，如果為1.0則兩字串完全相同才視為重複</br>

    Returns: 近期重複的訊息

    """
    job_msg = JobMsgPutRequest(raw_msg=raw_msg, auto_tag=True)
    await service.tag_if_needed(job_msg)
    return await service.find_duplicate_job_msgs(job_msg, db.job_msg, levenshtein_ratio)


@job_msg_router.get("/debug")
async def debug_job_msg(raw_msg: constr(min_length=20, max_length=2000, strip_whitespace=True),
                        current_user: CurrentUserDep) -> JobMsgDebugResponse:
    """除錯這則訊息，取得自動判別的行政區、醫師科別關鍵字與標籤"""
    return await service.debug_job_msg(raw_msg)


@job_msg_router.get("/{job_msg_id}")
async def get_job_msg_by_id(job_msg_id: str,
                            current_user: CurrentUserDep,
                            db: Database = Depends(database.get_db)) -> Optional[JobMsg]:
    """以job_msg_id查詢職缺訊息，此API不受時間範圍限制"""
    job_msg = await service.get_job_msg_by_id(job_msg_id, db.job_msg)
    if job_msg is None:
        raise HTTPException(status_code=404, detail=f"Job msg not found")
    return job_msg


@job_msg_router.get("")
async def get_job_msg(current_user: CurrentUserDep,
                      query: JobMsgQueryRequest = Depends(),
                      db: Database = Depends(database.get_db)) -> List[JobMsg]:
    """以時間及標籤條件查詢訊息，若要查詢第5筆到第7筆資料，則limit=3, skip=4</br>

    Note: 若city_tags和dept_tags都為空，會撈出較多訊息，給伺服器和資料庫造成負擔，不推薦這樣查詢</br>

    query.start_time: 起始時間，預設為近90日</br>
    end_time: 終止時間</br>
    city_tags: 行政區標籤，使用OR語意查詢，標籤上限為5個，若為空則全查</br>
    dept_tags: 醫師科別標籤，使用OR語意查詢，標籤上限為5個，若為空則全查</br>
    limit: 查詢結果筆數限制，0為不限制</br>
    skip: 跳過前n筆查詢</br>
    """
    return await service.get_job_msgs(query, db.job_msg)


@job_msg_router.delete("/{job_msg_id}")
async def delete_job_msg_by_id(job_msg_id: str,
                               current_user: CurrentUserDep,
                               db: Database = Depends(database.get_db)) -> JobMsgIdResponse:
    """以job_msg_id虛擬刪除職缺訊息，此API不受時間範圍限制"""
    res = await service.delete_job_msg_by_id(job_msg_id, current_user.user_id, db.job_msg)
    if not res:
        raise HTTPException(status_code=404, detail=f"Job msg not found")
    return JobMsgIdResponse(job_msg_id=job_msg_id)
