from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

DEFAULT_LNG = 80


class LocationDto(BaseModel):
    lat: int = Field(default=1, default_factory=None)
    lng: int = Field(default=DEFAULT_LNG)


class TypeEnum(Enum):
    ADMIN = 1
    USER = 2


class CreateUserDto(BaseModel):
    type: TypeEnum = Field(default=TypeEnum.USER, default_factory=None)
    name: str
    username: Optional[str] = Field(default=None, default_factory=None)


class UpdateUserDto(CreateUserDto):
    name: Optional[str]
    url: list[str] | list
    location: Optional[LocationDto]


class UserResponse(BaseModel):
    name: Optional[str]
