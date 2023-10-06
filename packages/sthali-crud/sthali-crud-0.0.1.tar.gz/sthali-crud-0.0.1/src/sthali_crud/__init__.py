from fastapi import APIRouter

from .config import config_router
from .crud import CRUD
from .schemas import Schema
from .types import App, Field, ResourceSpec


class SthaliCRUD:
    """SthaliCRUD
    """
    def __init__(self, app: App, resource_spec: ResourceSpec) -> None:
        schema = Schema(name=resource_spec.name, fields=resource_spec.fields)
        crud = CRUD(schema.response_model)
        resource_cfg = config_router(resource_spec, schema, crud)
        router = APIRouter(prefix=resource_cfg.prefix, tags=resource_cfg.tags)
        for route in resource_cfg.routes:
            router.add_api_route(
                path=route.path,
                endpoint=route.endpoint,
                response_model=route.response_model,
                methods=route.methods,
                status_code=route.status_code)
        app.include_router(router)


__all__ = [
    'SthaliCRUD',
    'ResourceSpec',
    'Field',
]
