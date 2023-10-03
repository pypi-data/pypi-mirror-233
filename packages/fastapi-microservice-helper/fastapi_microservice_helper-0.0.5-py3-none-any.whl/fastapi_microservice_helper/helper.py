from types import GenericAlias, UnionType
from typing import _UnionGenericAlias, Optional


def oneline(value: str):
    return value + '\r\n'


def tab(content: str, tabLength=1):
    tabContent = '    ' * tabLength
    newContent = ''
    for line in content.split('\r\n'):
        newContent += oneline(tabContent + line)

    return newContent


def get_generic_type(ref_type: type(GenericAlias)):
    alias_params = map(lambda ref: ref.__name__, ref_type.__args__)
    return f'{ref_type.__name__}[{",".join(alias_params)}]'


def get_optional_type(ref_type: type(_UnionGenericAlias)):
    alias_params = map(lambda ref: ref.__name__, filter(lambda ref: ref is not type(None), ref_type.__args__))
    return f'{ref_type.__name__}[{",".join(alias_params)}]'


def get_union_type(ref_type: type(UnionType)):
    alias_params = list[str]()
    for child_type in ref_type.__args__:
        if isinstance(child_type, GenericAlias):
            alias_params.append(get_generic_type(child_type))
        else:
            alias_params.append(child_type.__name__)
    return f'{" | ".join(alias_params)}'
