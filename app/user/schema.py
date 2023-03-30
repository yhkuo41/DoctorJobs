from __future__ import annotations

import re
from datetime import datetime
from typing import Optional, Mapping, Any

from pydantic import AnyStrMinLengthError, AnyStrMaxLengthError, BaseModel, SecretStr, StrRegexError, validator, \
    constr, EmailStr

from app.validator_util import get_content


class UserBase(BaseModel):
    """管理系統使用者，目前僅供管理員使用

    :param line_user_id: Line user id, can only be found in line msg api
    """
    account: str
    password: SecretStr
    email: EmailStr
    line_user_id: Optional[str]
    name: constr(min_length=1, max_length=50)

    @validator('account', 'password')
    def has_min_length(cls, v):
        min_length = 6
        if len(get_content(v)) < min_length:
            raise AnyStrMinLengthError(limit_value=min_length)
        return v

    @validator('account', 'password')
    def has_max_length(cls, v):
        max_length = 50
        if len(get_content(v)) > max_length:
            raise AnyStrMaxLengthError(limit_value=max_length)
        return v

    @validator('account', 'password')
    def matches_regex(cls, v):
        regex = r'\w+'
        if not re.match(regex, get_content(v)):
            raise StrRegexError(pattern=regex)
        return v


class User(UserBase):
    user_id: str
    create_ts: datetime
    """create timestamp (UTC)"""
    update_ts: datetime
    """update timestamp (UTC)"""
    is_delete: bool

    @classmethod
    def from_mapping(cls, res: Mapping[str, Any]) -> Optional[User]:
        if res is None:
            return
        return User(
            user_id=str(res['_id']),
            account=res['account'],
            password=res['password'],
            email=res['email'],
            line_user_id=res['line_user_id'],
            name=res['name'],
            create_ts=res['create_ts'],
            update_ts=res['update_ts'],
            is_delete=res['is_delete']
        )

    # no need to verify account & password when fetch data from db
    @validator('account', 'password')
    def has_max_length(cls, v):
        return v

    @validator('account', 'password')
    def matches_regex(cls, v):
        return v


class UserCreateResponse(BaseModel):
    id: str
