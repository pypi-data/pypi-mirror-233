from enum import Enum

from pydantic import BaseModel, Field, TypeAdapter


class OldTypeEnum(Enum):
    ADMIN = Field(default=1)
    USER = Field(default=1)


class TypeEnum(Enum):
    ADMIN = 1
    USER = 2


class User(BaseModel):
    username: str
    type: TypeEnum


print(TypeAdapter(User).validate_python({'username': 'John', 'type': 1}))
