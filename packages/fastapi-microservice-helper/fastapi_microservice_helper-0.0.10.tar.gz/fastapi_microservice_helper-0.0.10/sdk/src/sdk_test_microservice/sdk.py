from pydantic import BaseModel,Field
from dataclasses import dataclass,field
from enum import Enum
from typing import Any,Optional
from uuid import UUID

class UserResponse(BaseModel):
    name: Optional[str]

class TypeEnum(Enum):
    ADMIN=Field(default=1)

    USER=Field(default=2)

class LocationDto(BaseModel):
    lat: int=Field(default=1)

    lng: int=Field(default=80)

class UpdateUserDto(BaseModel):
    name: Optional[str]

    username: Optional[str]

    url: list[str] | list

    location: Optional[LocationDto]

    type: TypeEnum=Field(default=TypeEnum.USER)
    
    

from dataclasses import dataclass
from inspect import isclass

import httpx
from fastapi import HTTPException
from pydantic import BaseModel


@dataclass
class MicroserviceOption:
    is_json: bool = True
    headers: dict = None


@dataclass
class SdkTestMicroserviceConfig:
    url: str


class BaseMicroserviceClient:
    async def send(self, url: str, query_params: dict, body_params: any, response_type: any,
                   option: MicroserviceOption = None):
        if not SdkTestMicroserviceConfig.url:
            raise Exception("Please config microservice url")

        url = SdkTestMicroserviceConfig.url + url
        if not option:
            option = MicroserviceOption()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=url,
                headers=option.headers,
                params=query_params,
                data=body_params if not option.is_json else None,
                json=body_params if option.is_json else None,
            )
            data = response.json()
            if response.status_code < 200 or response.status_code > 299:
                raise HTTPException(status_code=response.status_code, detail=data)
            if not response_type:
                return data

            if isclass(response_type) and issubclass(response_type, BaseModel):
                return response_type.model_validate(data)

            return response_type(data)

class Microservice(BaseMicroserviceClient):
    async def get_user_by_id(self, user_id: UUID, option: MicroserviceOption = None) -> UserResponse:
        return await self.send('/microservices/Microservice/get_user_by_id', {'user_id': user_id}, None, UserResponse, option )
    
    

    async def test(self, user_id: UUID, dto: UpdateUserDto, option: MicroserviceOption = None) -> None:
        return await self.send('/microservices/Microservice/test', {'user_id': user_id}, dto, None, option )
    
    

    async def update_user(self, user_id: UUID, dto: UpdateUserDto, option: MicroserviceOption = None) -> UserResponse:
        return await self.send('/microservices/Microservice/update_user', {'user_id': user_id}, dto, UserResponse, option )
