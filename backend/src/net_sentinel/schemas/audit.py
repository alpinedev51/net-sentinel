from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AuditBase(BaseModel):
    """Base fields shared across multiple Audit schemas."""

    is_active: bool = Field(default=True)


class AuditCreate(AuditBase):
    """Schema for validating data received in a POST request."""

    pass


class AuditResponse(AuditBase):
    """Schema for serializing data sent back to the client."""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
