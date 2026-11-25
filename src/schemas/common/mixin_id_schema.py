from typing import Optional
from pydantic import Field
from .base_schema import BaseSchema


class MixinIdSchema(BaseSchema):
    id: Optional[int] = Field(default=None, ge=1, description='ID')