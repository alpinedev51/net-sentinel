from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AuditBase(BaseModel):
    """Base fields shared across multiple Audit schemas."""

    name: str = Field(..., max_length=255, description="The name of the audit campaign.")
    description: str | None = Field(default=None)


class AuditCreate(AuditBase):
    """Schema for validating data received in a POST request."""
    target_ids: list[int] = Field(..., min_length=1, description="List of target IDs to scan.")
    tools: list[int] = Field(..., min_length=1, description="List of tools to use (e.g., nmap, ping).")


class AuditResponse(AuditBase):
    """Schema for serializing data sent back to the client."""

    id: int
    status: str
    created_at: datetime
    started_at: datetime
    completed_at: datetime

    model_config = ConfigDict(from_attributes=True)
