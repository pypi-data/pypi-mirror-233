from enum import Enum
from typing import Any, Callable, List, Literal, Optional, Set, Union

from fastapi import FastAPI
from pydantic.dataclasses import dataclass


@dataclass
class App(FastAPI):
    """App

    Args:
        FastAPI (_type_): _description_
    """


@dataclass
class Field:
    """Field
    """
    name: str
    type: type
    default: Any = None
    allow_none: bool = False


@dataclass
class ResourceSpec:
    """ResourceSpec
    """
    name: str
    fields: List[Field]


@dataclass
class RouteConfig:
    """RouteConfig
    """
    path: str
    endpoint: Callable[..., Any]
    response_model: Any
    methods: Optional[Union[
        Set[Literal['GET', 'POST', 'PUT', 'PATCH', 'DELETE']],
        List[Literal['GET', 'POST', 'PUT', 'PATCH', 'DELETE']]
    ]] = None
    status_code: int = 200


@dataclass
class ResourceCfg:
    """ResourceCfg
    """
    prefix: str
    routes: List[RouteConfig]
    tags: Optional[List[Union[str, Enum]]] = None
