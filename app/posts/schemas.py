from pydantic import BaseModel, HttpUrl
from typing import Optional, List


class PostCreate(BaseModel):
    platform: str
    content: str

    post_url: Optional[HttpUrl] = None
    author_name: Optional[str] = None
    author_role: Optional[str] = None
    company: Optional[str] = None

    industry: Optional[str] = None
    topic_tags: Optional[List[str]] = None


class PostResponse(BaseModel):
    id: int
    platform: str
    content: str

    class Config:
        from_attributes = True

class PostIngestRequest(BaseModel):
    platform: str
    content: str

    author_name: Optional[str] = None
    author_role: Optional[str] = None
    company: Optional[str] = None
    post_url: Optional[str] = None
