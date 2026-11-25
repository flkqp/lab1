from datetime import datetime
from typing import Optional
from pydantic import Field
from .base_schema import BaseSchema


class MixinSoftDeleteSchema(BaseSchema):
    is_deleted: bool = Field(default=False)
    deleted_by: Optional[int] = Field(default=None)
    deleted_at: Optional[datetime] = Field(default=None)