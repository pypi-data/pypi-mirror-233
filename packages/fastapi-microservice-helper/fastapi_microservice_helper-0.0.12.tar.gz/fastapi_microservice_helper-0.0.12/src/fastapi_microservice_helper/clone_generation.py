import dataclasses
from dataclasses import _MISSING_TYPE
from enum import Enum
from inspect import isclass
from types import GenericAlias, UnionType
from typing import _UnionGenericAlias

from pydantic._internal._model_construction import ModelMetaclass
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

from .code_generation import Generation
from .helper import get_generic_type, get_optional_type, get_union_type
from .models.generation_detail import GenerationClassDetail, GenerationPropertyDetail


class CloneGeneration:
    def clone_class_to_dataclass(self, ref_class):
        if type(ref_class) is ModelMetaclass:
            class_detail = GenerationClassDetail(
                class_name=ref_class.__name__, is_dataclass=False, parent_name='BaseModel'
            )
            for key in ref_class.__fields__.keys():
                property_detail = self.clone_model_field(key, ref_class.__fields__[key])
                class_detail.properties.append(property_detail)

            self.sort_properties(class_detail)
            return Generation().generate(class_detail)
        else:
            if isclass(ref_class) and issubclass(ref_class, Enum):
                return self.clone_enum(ref_class)
            elif dataclasses.is_dataclass(ref_class):
                return self.clone_dataclass(ref_class)
            else:
                print(type(ref_class))
                print("Need to implement this type", ref_class)

        return ''

    def clone_model_field(self, name: str, property: FieldInfo):
        default_value = property.default if property.default is not PydanticUndefined else None
        property_detail = GenerationPropertyDetail(
            name,
            type=self.get_type_name(property),
            default_value=default_value,
            default_factory=property.default_factory,
        )

        return property_detail

    def get_type_name(self, property: FieldInfo):
        if type(property.annotation) is UnionType:
            return get_union_type(property.annotation)

        if type(property.annotation) is _UnionGenericAlias:
            return get_optional_type(property.annotation)

        if isinstance(property.annotation, GenericAlias):
            return get_generic_type(property.annotation)

        return property.annotation.__name__

    def clone_enum(self, ref_class: type[Enum]):
        class_detail = GenerationClassDetail(class_name=ref_class.__name__, parent_name=Enum.__name__)
        for member in ref_class:
            class_detail.properties.append(
                GenerationPropertyDetail(name=member.name, default_value=member.value, is_enum=True)
            )
        return Generation().generate(class_detail)

    def clone_dataclass(self, ref_class: type[dataclasses]):
        class_detail = GenerationClassDetail(class_name=ref_class.__name__, is_dataclass=True)
        for field in dataclasses.fields(ref_class):
            type_name = field.type.__name__
            if isinstance(field.type, GenericAlias):
                type_name = get_generic_type(field.type)
            property_detail = GenerationPropertyDetail(
                name=field.name,
                type=type_name,
                default_value=field.default if not type(field.default) is _MISSING_TYPE else None,
                default_factory=field.default_factory if not type(field.default_factory) is _MISSING_TYPE else None,
            )
            class_detail.properties.append(property_detail)
        self.sort_properties(class_detail)
        return Generation().generate(class_detail)

    def sort_properties(self, class_detail: GenerationClassDetail):
        def sort_property(property):
            if property.default_value:
                return 1
            if property.default_value is None and property.allow_none:
                return 1
            elif property.default_factory:
                return 1
            return 0

        class_detail.properties.sort(key=sort_property)
