"""Define base and common pydantic models"""

from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field


class Base(BaseModel):
    """Base model reference"""
    model_config = ConfigDict(extra="allow")


class ResponseModel(Base):
    code: str  # '200'
    message: str  # 'Operation success',
    status: str  # 'success',
    version: str  # '2'


class Link(Base):
    first: Optional[str] = None  # http://hostname/api/nodes?page=1
    last: Optional[str] = None  # http://hostname/api/nodes?page=1
    prev: Optional[str] = None  # number | null
    next: Optional[str] = None  # number | null


class Link2(Base):
    url: Optional[str] = None
    label: Optional[str] = None
    active: bool


class Meta(BaseModel):
    """Similar to other Meta models"""
    current_page: Optional[int] = None  # 1,
    from_: Optional[int] = Field(None, alias='from')  # 1,
    last_page: Optional[int] = None  # 1,
    path: Optional[str] = None  # http://hostname/api/nodes,
    per_page: Optional[int] = None  # 15,
    to: Optional[int] = None  # 2,
    total: Optional[int] = None  # 2,
    all_count: Optional[int] = None  # number,
    filter_count: Optional[int] = None  # number
    links: Optional[List[Link2]] = None
