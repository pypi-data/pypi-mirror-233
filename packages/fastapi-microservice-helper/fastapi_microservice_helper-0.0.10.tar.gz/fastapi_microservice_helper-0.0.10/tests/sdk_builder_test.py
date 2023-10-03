import os
import sys
from uuid import UUID

from fastapi import FastAPI
from fastapi_global_variable import GlobalVariable
from fastapi_request_helper.decorators.http_method import response

app_dir = os.path.abspath(os.path.dirname(__file__)) + '/..'
if app_dir not in sys.path:
    sys.path.append(app_dir)

from src.fastapi_microservice_helper import microservice, action, SdkBuilder
from src.fastapi_microservice_helper.clone_generation import CloneGeneration
from tests.dto import UpdateUserDto, LocationDto, UserResponse

app = FastAPI(title="pixerpost API")
GlobalVariable.set('app', app)


@microservice()
class Microservice:

    @action()
    @response(UserResponse)
    async def get_user_by_id(self, user_id: UUID):
        return {
            'name': 'Dzung'
        }

    @action()
    @response(UserResponse)
    async def update_user(self, user_id: UUID, dto: UpdateUserDto):
        return {
            'name': 'Dzung'
        }

    @action()
    @response(None)
    async def test(self, user_id: UUID, dto: UpdateUserDto):
        return {
            'name': 'Dzung'
        }


SdkBuilder().generate(app.routes)
