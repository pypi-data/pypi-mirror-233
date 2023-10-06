from dataclasses import dataclass

from pydantic_core.core_schema import ModelField


@dataclass
class MethodDetail:
    class_name: str
    path: str
    function_name: str
    query_params: list[ModelField]
    body_params: list[ModelField]
    parameters_position: list
    response_field: ModelField
