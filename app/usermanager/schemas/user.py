from typing import Union, List, Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    first_name: str = Field(..., max_length=50, min_length=1)
    middle_name: str = Field(..., max_length=50, min_length=1)
    last_name: str = Field(..., max_length=50, min_length=1)


class UserPartialUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50, min_length=1)
    middle_name: Optional[str] = Field(None, max_length=50, min_length=1)
    last_name: Optional[str] = Field(None, max_length=50, min_length=1)


class UserOutput(User):
    id: Union[str, int]
