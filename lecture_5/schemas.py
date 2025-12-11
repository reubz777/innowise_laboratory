from typing import Optional

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    year: Optional[int] = None


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int

    class Config:
        from_attributes = True
