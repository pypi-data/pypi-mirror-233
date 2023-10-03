from dataclasses import dataclass
from inspect import isclass

from fastapi import HTTPException
import httpx
from pydantic import BaseModel


@dataclass
class MicroserviceOption:
    is_json: bool = True
    headers: dict = None


@dataclass
class ReplaceMicroserviceConfig:
    url: str


class BaseMicroserviceClient:
    async def send(self, url: str, query_params: dict, body_params: any, response_type: any,
                   option: MicroserviceOption = None):
        if not ReplaceMicroserviceConfig.url:
            raise Exception("Please config microservice url")

        url = ReplaceMicroserviceConfig.url + url
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
