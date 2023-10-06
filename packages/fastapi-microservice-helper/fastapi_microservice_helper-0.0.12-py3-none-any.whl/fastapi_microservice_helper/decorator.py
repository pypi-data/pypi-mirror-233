from typing import Callable, Type, TypeVar

from fastapi_global_variable import GlobalVariable
from fastapi_request_helper.constants.http_method import POST
from fastapi_request_helper.decorators.controller import add_function_routers
from fastapi_request_helper.helpers.router_decorator import set_api_detail
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

T = TypeVar('T')


def action():
    def decorator(cls: Type[T]):
        set_api_detail(cls, 'methods', [POST])
        set_api_detail(cls, 'path', '/' + cls.__name__)
        return cls

    return decorator


def microservice() -> Callable[[Type[T]], Type[T]]:
    def decorator(cls: Type[T]) -> Type[T]:
        router = InferringRouter()
        prefix = f'microservices/{cls.__name__}'
        add_function_routers(prefix, cls, router)
        cbv(router)(cls)
        GlobalVariable.get_or_fail('app').include_router(router)

        return cls

    return decorator
