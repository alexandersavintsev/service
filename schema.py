from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserGet(BaseModel):
    id: int
    age: Optional[int]
    city: Optional[str]
    country: Optional[str]
    exp_group: Optional[int]
    gender: Optional[int]
    os: Optional[str]
    source: Optional[str]

    class Config:
        orm_mode = True


class PostGet(BaseModel):
    id: int
    text: Optional[str]
    topic: Optional[str]

    class Config:
        orm_mode = True


class FeedGet(BaseModel):
    user_id: int
    post_id: int
    action: Optional[str]
    time: Optional[datetime]

    user: Optional[UserGet]
    post: Optional[PostGet]

    class Config:
        orm_mode = True
