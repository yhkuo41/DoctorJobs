from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional, Mapping, Any

from fastapi import Query
from pydantic import BaseModel, constr, conint, EmailStr, root_validator, Field

from app.job_msg.tagger.city import City
from app.job_msg.tagger.dept import Dept

QUERY_TIME_LIMIT = timedelta(days=90)


def recent_ts() -> datetime:
    return datetime.utcnow() - QUERY_TIME_LIMIT


class ContactInfo(BaseModel):
    telephone: Optional[constr(min_length=8, max_length=20)]
    email: Optional[EmailStr]
    contact_person: Optional[constr(min_length=1, max_length=50)]

    @classmethod
    def from_mapping(cls, res: Mapping[str, Any]) -> Optional[ContactInfo]:
        if res is None:
            return
        return ContactInfo(
            telephone=res['telephone'],
            email=res['email'],
            contact_person=res['contact_person']
        )

    def to_mapping(self) -> dict[str:Any]:
        return {
            "telephone": self.telephone,
            "email": self.email,
            "contact_person": self.contact_person,
        }

    class Config:
        anystr_strip_whitespace = True  # remove trailing whitespace


class JobMsgBase(BaseModel):
    """職缺訊息及摘要</br>
    :param raw_msg: 原始訊息</br>
    :param city_tags: 行政區標籤</br>
    :param dept_tags: 醫師科別標籤</br>
    :param contact_info: 聯絡資訊</br>
    :param company: 公司名稱</br>
    :param job_desc: 工作內容</br>
    :param salary_desc: 薪資待遇</br>
    :param working_hours: 工作時間</br>
    """
    raw_msg: constr(min_length=20, max_length=4096)
    city_tags: set[City] = set()
    dept_tags: set[Dept] = set()
    contact_info: Optional[ContactInfo]
    company: Optional[constr(min_length=1, max_length=256)]
    job_desc: Optional[constr(min_length=1, max_length=4096)]
    salary_desc: Optional[constr(min_length=1, max_length=256)]
    working_hours: Optional[constr(min_length=1, max_length=256)]

    def contact_info_to_mapping(self) -> Optional[dict[str:Any]]:
        if self.contact_info:
            return self.contact_info.to_mapping()

    class Config:
        anystr_strip_whitespace = True  # remove trailing whitespace


class JobMsgPutRequest(JobMsgBase):
    """職缺訊息及摘要</br>
    Note: 非自動標記時，行政區標籤及醫師科別標籤兩者不能都為空，否則無法有效過濾查詢；自動標記時，若標記後兩者皆為空，則會拋出例外</br>
    :param raw_msg: 原始訊息</br>
    :param job_msg_id: 如果有job_msg_id，則會直接對此ID進行更新，否則為新增</br>
    :param auto_tag: 自動標記，將根據原始訊息，清除輸入的標籤，並自動打上新的行政區與醫師科別標籤</br>
    :param city_tags: 行政區標籤</br>
    :param dept_tags: 醫師科別標籤</br>
    :param contact_info: 聯絡資訊</br>
    :param company: 公司名稱</br>
    :param job_desc: 工作內容</br>
    :param salary_desc: 薪資待遇</br>
    :param working_hours: 工作時間
    """
    job_msg_id: Optional[str]
    auto_tag: bool = True

    def to_update_mapping(self, now: datetime, current_user_id: str) -> dict[str:Any]:
        return {
            "raw_msg": self.raw_msg,
            "city_tags": [e.value for e in self.city_tags],
            "dept_tags": [e.value for e in self.dept_tags],
            "contact_info": self.contact_info_to_mapping(),
            "company": self.company,
            "job_desc": self.job_desc,
            "salary_desc": self.salary_desc,
            "working_hours": self.working_hours,
            "update_ts": now,
            "update_by": current_user_id,
        }

    def to_insert_mapping(self, now: datetime, current_user_id: str) -> dict[str:Any]:
        res = self.to_update_mapping(now, current_user_id)
        res.update({
            "update_ts": now,
            "create_by": current_user_id,
            "update_by": current_user_id,
            "is_delete": False
        })
        return res

    @staticmethod
    def to_delete_mapping(now: datetime, current_user_id: str) -> dict[str:Any]:
        return {
            "update_ts": now,
            "update_by": current_user_id,
            "is_delete": True
        }


class JobMsg(JobMsgBase):
    job_msg_id: str
    create_ts: datetime
    update_ts: datetime
    create_by: Optional[str]
    update_by: Optional[str]
    is_delete: bool

    @classmethod
    def from_mapping(cls, res: Mapping[str, Any]) -> Optional[JobMsg]:
        if res is None:
            return
        return JobMsg(
            job_msg_id=str(res['_id']),
            raw_msg=res['raw_msg'],
            city_tags=res['city_tags'],
            dept_tags=res['dept_tags'],
            contact_info=ContactInfo.from_mapping(res['contact_info']),
            company=res['company'],
            job_desc=res['job_desc'],
            salary_desc=res['salary_desc'],
            working_hours=res['working_hours'],
            create_ts=res['_id'].generation_time,
            update_ts=res['update_ts'],
            create_by=res['create_by'],
            update_by=res['update_by'],
            is_delete=res['is_delete']
        )


class JobMsgQueryRequest(BaseModel):
    start_time: Optional[datetime] = recent_ts()
    end_time: Optional[datetime]
    city_tags: set[City] = Field(Query(set()), max_items=5)
    dept_tags: set[Dept] = Field(Query(set()), max_items=5)
    limit: conint(ge=0) = 0
    skip: conint(ge=0) = 0

    @root_validator()
    def validate_all_fields(cls, field_values):
        if field_values["end_time"] and field_values["end_time"] <= field_values["start_time"]:
            raise ValueError("end_time can not before or equals to start_time")
        return field_values


class JobMsgIdResponse(BaseModel):
    job_msg_id: str


class JobMsgDebugResponse(BaseModel):
    """職缺除錯訊息</br>
    :param raw_msg: 原始訊息</br>
    :param keyword_to_cites: 關鍵字 to 行政區</br>
    :param keyword_to_depts: 關鍵字 to 科別列表</br>
    :param keyword_to_neg_depts: 反向關鍵字 to 科別列表，排除過濾用</br>
    """
    raw_msg: constr(min_length=20, max_length=4096)
    keyword_to_cites: dict = {}
    keyword_to_depts: dict = {}
    keyword_to_neg_depts: dict = {}
