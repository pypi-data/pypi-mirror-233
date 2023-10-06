from pydash import group_by

from .helper import oneline, tab
from .models.generation_detail import (GenerationClassDetail, GenerationImportModuleDetail, GenerationMethodDetail,
                                       GenerationPropertyDetail)


class Generation:
    def generate(self, class_detail: GenerationClassDetail):
        return self.generate_class(class_detail)

    def generate_import_modules(self, list_import_module: list[GenerationImportModuleDetail]):
        content = ''
        import_modules = group_by(list_import_module, 'module')
        for key in import_modules.keys():
            types = map(lambda import_module: import_module.type, import_modules[key])
            content += oneline(f'from {key} import {",".join(types)}')
        return content

    def generate_class(self, class_detail: GenerationClassDetail):
        parent_name = f'({class_detail.parent_name})' if class_detail.parent_name else ''
        content = oneline('@dataclass') if class_detail.is_dataclass else ''
        content += oneline(f'class {class_detail.class_name}{parent_name}:')
        content += self.generate_properties(class_detail.properties)
        content += self.generate_methods(class_detail.methods)
        return content

    def generate_methods(self, methods: list[GenerationMethodDetail]):
        content = ''
        for method in methods:
            content += tab(self.generate_method(method))
            content += '\r\n'
        return content

    def generate_method(self, method: GenerationMethodDetail):
        paramList = ", ".join(map(lambda param: f'{param.name}: {param.type}', method.params))
        content = oneline(
            f'async def {method.name}(self, {paramList}, option: MicroserviceOption = None) -> {method.response}:'
        )
        content += oneline(tab(method.body))

        return content

    def generate_properties(self, properties: list[GenerationPropertyDetail]):
        content = ''
        for property in properties:
            content += tab(self.generate_property(property))
            content += '\r\n'
        return content

    def generate_property(self, property: GenerationPropertyDetail):
        if property.is_enum:
            return f'{property.name} = {property.default_value}'

        content = f'{property.name}: {property.type}' if property.type else property.name

        fields = list()
        if property.default_value:
            fields.append(f'default={property.default_value}')
        if property.default_value is None and property.allow_none:
            fields.append(f'default=None')
        elif property.default_factory:
            fields.append(f'default_factory={property.default_factory}')

        if fields:
            content += f'=Field({",".join(fields)})'

        return content
