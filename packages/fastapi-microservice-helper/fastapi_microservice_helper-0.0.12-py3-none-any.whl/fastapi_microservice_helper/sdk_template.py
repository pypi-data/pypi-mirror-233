import dataclasses
from dataclasses import is_dataclass
from types import GenericAlias, UnionType
from typing import Dict, _UnionGenericAlias, get_args

import pydash
from pydantic._internal._model_construction import ModelMetaclass
from pydantic.fields import FieldInfo
from pydantic_core.core_schema import ModelField
from pydash import some

from .clone_generation import CloneGeneration
from .code_generation import (Generation, GenerationClassDetail, GenerationImportModuleDetail, GenerationMethodDetail,
                              GenerationPropertyDetail)
from .helper import get_generic_type, oneline
from .models.method_detail import MethodDetail


class SdkTemplate:
    def generate_method(self, method_detail: MethodDetail):
        params: list[ModelField] = list(method_detail.query_params + method_detail.body_params)
        params.sort(key=lambda param: method_detail.parameters_position.index(param.name))

        return GenerationMethodDetail(
            name=method_detail.function_name,
            response=self.get_response(method_detail),
            body=self.get_method_body(method_detail),
            params=list(map(lambda param: GenerationPropertyDetail(param.name, param.type_.__name__), params)),
        )

    def get_method_body(self, method_detail: MethodDetail):
        body_params = [f"'{method_detail.path}'"]

        if method_detail.query_params:
            query_params = ', '.join(map(lambda query: f"'{query.name}': {query.name}", method_detail.query_params))
            body_params.append('{' + query_params + '}')
        else:
            body_params.append('None')

        if method_detail.body_params:
            body_params.append(method_detail.body_params[0].name)
        else:
            body_params.append('None')

        return f'return await self.send({", ".join(body_params)}, {self.get_response(method_detail)}, option )'

    def get_response(self, method_detail: MethodDetail):
        if not method_detail.response_field:
            return 'None'
        response_name = method_detail.response_field.type_.__name__
        if isinstance(method_detail.response_field.type_, GenericAlias):
            return get_generic_type(method_detail.response_field.type_)
        return response_name

    def generate_class(self, name, methods: list[MethodDetail]):
        class_detail = GenerationClassDetail(class_name=name, parent_name='BaseMicroserviceClient')
        for method in methods:
            class_detail.methods.append(self.generate_method(method))
        return Generation().generate(class_detail)

    def generate_ref_class(self, microservice: Dict):
        list_ref_class = list()
        list_import_module: list[GenerationImportModuleDetail] = list(
            (
                GenerationImportModuleDetail('pydantic', 'BaseModel'),
                GenerationImportModuleDetail('pydantic', 'Field'),
                GenerationImportModuleDetail('dataclasses', 'dataclass'),
                GenerationImportModuleDetail('dataclasses', 'field'),
                GenerationImportModuleDetail('enum', 'Enum'),
                GenerationImportModuleDetail('typing', 'Any'),
                GenerationImportModuleDetail('typing', 'Optional'),
            )
        )
        for key in microservice.keys():
            methods: list[MethodDetail] = microservice[key]
            for method in methods:
                for body in method.body_params:
                    self.get_list_ref_class(body.type_, list_ref_class, list_import_module)
                for query in method.query_params:
                    self.get_list_ref_class(query.type_, list_ref_class, list_import_module)
                if method.response_field:
                    self.get_list_ref_class(method.response_field.type_, list_ref_class, list_import_module)

        content = oneline(Generation().generate_import_modules(list_import_module))
        list_ref_class = pydash.filter_(list_ref_class, lambda ref_class: not isinstance(ref_class, GenericAlias))

        for ref_class in list_ref_class:
            content += CloneGeneration().clone_class_to_dataclass(ref_class)
        return content

    def get_list_ref_class(
        self, ref_type, list_ref_class: list, list_import_module: list[GenerationImportModuleDetail]
    ):
        if type(ref_type) is UnionType:
            for child_type in get_args(ref_type):
                self.get_list_ref_class(child_type, list_ref_class, list_import_module)
            return
        if type(ref_type) is _UnionGenericAlias:
            for child_type in get_args(ref_type):
                self.get_list_ref_class(child_type, list_ref_class, list_import_module)
            return
        if some(
            list_import_module,
            lambda import_module: import_module.type == ref_type.__qualname__
            and import_module.module == ref_type.__module__,
        ):
            return
        if type(ref_type) is type and not is_dataclass(ref_type):
            if ref_type.__module__ != 'builtins':
                list_import_module.append(GenerationImportModuleDetail(ref_type.__module__, ref_type.__qualname__))
            return
        if ref_type in list_ref_class:
            return
        list_ref_class.append(ref_type)

        if type(ref_type) is ModelMetaclass:
            for key in ref_type.__fields__.keys():
                property: FieldInfo = ref_type.__fields__[key]
                self.get_list_ref_class(property.annotation, list_ref_class, list_import_module)
        elif is_dataclass(ref_type):
            for field in dataclasses.fields(ref_type):
                self.get_list_ref_class(field.type, list_ref_class, list_import_module)
        elif isinstance(ref_type, GenericAlias):
            for alias in ref_type.__args__:
                self.get_list_ref_class(alias, list_ref_class, list_import_module)
