import typing
from dataclasses import dataclass, field


@dataclass
class GenerationImportModuleDetail:
    module: str
    type: str


@dataclass
class GenerationPropertyDetail:
    name: str
    type: typing.Optional[str] = None
    default_value: typing.Optional[any] = None
    default_factory: typing.Optional[any] = None
    allow_none: bool = False
    is_enum: bool = False


@dataclass
class GenerationMethodDetail:
    name: str
    params: list[GenerationPropertyDetail] = field(default_factory=list)
    body: str = None
    response: str = None


@dataclass
class GenerationClassDetail:
    class_name: str
    parent_name: str = None
    methods: list[GenerationMethodDetail] = field(default_factory=list)
    properties: list[GenerationPropertyDetail] = field(default_factory=list)
    is_dataclass: bool = False
