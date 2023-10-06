from typing import List

from .crud import CRUD
from .schemas import Schema
from .types import ResourceCfg, ResourceSpec, RouteConfig


def replace_type_hint(original_func, type_names, new_type):
    """replace_type_hint
    """
    for name in type_names:
        original_func.__annotations__[name] = new_type
    return original_func


def config_router(resource_spec: ResourceSpec, schema: Schema, crud: CRUD) -> ResourceCfg:
    """config_router

    Args:
        resource_spec (ResourceSpec): _description_
        schema (Schema): _description_
        crud (CRUD): _description_

    Returns:
        ResourceCfg: _description_
    """

    response_model = schema.response_model
    return ResourceCfg(
        prefix=f'/{resource_spec.name}',
        routes=[
            RouteConfig(
                path='/',
                endpoint=replace_type_hint(crud.create, ['resource', 'return'], response_model),
                response_model=response_model,
                methods=['POST'],
                status_code=201),
            RouteConfig(
                path='/{resource_id}/',
                endpoint=crud.read,
                response_model=response_model,
                methods=['GET']),
            # RouteConfig(
            #     path='/',
            #     endpoint=crud.read_all,
            #     response_model=List[response_model],
            #     methods=['GET']),
            RouteConfig(
                path='/{resource_id}/',
                endpoint=replace_type_hint(crud.update, ['resource', 'return'], response_model),
                response_model=response_model,
                methods=['PATCH']),
            # RouteConfig(
            #     path='/{resource_id}/',
            #     endpoint=crud.upsert,
            #     response_model=response_model,
            #     methods=['PUT']),
            RouteConfig(
                path='/{resource_id}/',
                endpoint=crud.delete,
                response_model=None,
                methods=['DELETE'],
                status_code=204)
                ],
        tags=[resource_spec.name]
    )
