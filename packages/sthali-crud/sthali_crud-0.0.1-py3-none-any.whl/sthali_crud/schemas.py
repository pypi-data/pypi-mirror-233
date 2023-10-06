from typing import Any, List, Optional

from pydantic import BaseModel, create_model

from .types import Field


class Schema(BaseModel):
    """Schema
    """
    name: str
    fields: List[Field]

    @property
    def response_model(self) -> Any:
        """response_model
        """
        return create_model(
            self.name,
            **{field.name: ((field.type, Optional[field.type])[field.allow_none], field.default or ...)
               for field in self.fields})  # type: ignore
