import os
from inspect import getsourcefile
from shutil import copy, rmtree, copyfile
from typing import Dict

import toml
from fastapi.routing import APIRoute
from pydash import group_by
from ssort import ssort
from starlette.routing import BaseRoute

from .base_microservice_client import BaseMicroserviceClient
from .models.method_detail import MethodDetail
from .sdk_template import SdkTemplate


class SdkBuilder:
    def generate(self, routes: list[BaseRoute]) -> None:
        root_path = os.path.abspath('.')
        sdk_path = os.path.join(root_path, 'sdk')
        self.create_sdk_dir(sdk_path)
        self.clone_static_files(root_path, sdk_path)
        sdk_detail = self.get_sdk_detail(root_path)
        project_name = sdk_detail['project']['name']
        self.create_source_dir(sdk_path, project_name)
        source_path = os.path.join(sdk_path, 'src', project_name)
        self.generate_init_file(source_path)
        self.generate_code(project_name, source_path, routes)

    def get_sdk_detail(self, root_path: str):
        with open(os.path.join(root_path, 'sdk.toml'), 'r') as file:
            return toml.load(file)

    def create_sdk_dir(self, sdk_path: str):
        if os.path.exists(sdk_path):
            rmtree(sdk_path)
        os.mkdir(sdk_path)

    def create_source_dir(self, sdk_path: str, project_name: str):
        src_path = os.path.join(sdk_path, 'src')
        os.mkdir(src_path)
        os.mkdir(os.path.join(src_path, project_name))

    def generate_init_file(self, source_path: str):
        content = 'from .sdk import *'
        with open(os.path.join(source_path, '__init__.py'), "w+") as file:
            file.write(content)

    def clone_static_files(self, root_path: str, sdk_path: str):
        files = ['.gitignore']
        for file in files:
            file_path = os.path.join(root_path, file)

            if not os.path.exists(file_path):
                raise Exception(f'{file} not exists in root folder.')
            copy(file_path, sdk_path)

        if not os.path.exists(os.path.join(root_path, 'sdk.toml')):
            raise Exception('sdk.toml not exists in root folder.')
        copyfile(os.path.join(root_path, 'sdk.toml'), os.path.join(sdk_path, 'pyproject.toml'))

    def generate_code(self, name: str, source_path: str, routes: list[BaseRoute]):
        microservices = list()
        for route in routes:
            if isinstance(route, APIRoute):
                if route.path.startswith('/microservices/'):
                    microservices.append(self.get_api_detail(route))

        microservice = group_by(microservices, 'class_name')
        self.create_file(name, source_path, microservice)

    def get_api_detail(self, route: APIRoute):
        qualified_name: str = route.endpoint.__qualname__
        parameters_position = list(route.endpoint.__code__.co_varnames)
        parameters_position.remove('self')

        if len(route.dependant.body_params) > 1:
            raise Exception('Cannot use more than 1 dto for microservices.')

        method_detail = MethodDetail(
            path=route.path,
            class_name=qualified_name.split('.')[0],
            function_name=qualified_name.split('.')[1],
            query_params=route.dependant.query_params,
            body_params=route.dependant.body_params,
            parameters_position=parameters_position,
            response_field=route.response_field
        )
        return method_detail

    def create_file(self, name: str, source_path: str, microservice: Dict):
        sdk_template = SdkTemplate()
        content = ''''''
        content += sdk_template.generate_ref_class(microservice)
        for key in microservice.keys():
            content += sdk_template.generate_class(key, microservice[key])
        with open(getsourcefile(BaseMicroserviceClient), 'r') as file:
            content += file.read()
        content = content.replace(
            'ReplaceMicroserviceConfig',
            f'{name.replace("_", " ").replace("-", " ").title().replace(" ", "")}Config'
        )
        file_content = ssort(content)
        with open(os.path.join(source_path, 'sdk.py'), "w+") as file:
            file.write(file_content)
