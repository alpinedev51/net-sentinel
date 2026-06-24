from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, ConfigDict, Field


class TargetBase(BaseModel):
    """Base fields shared across multiple Target schemas."""

    ip_address: str = Field(..., max_length=45, description="Supports IPv4 and IPv6.")
    hostname: str | None = Field(default=None, max_length=255)
    mac_address: str | None = Field(default=None, max_length=17)
    label: str | None = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)


class TargetCreate(TargetBase):
    """Schema for validating data received in a POST request."""

    pass


class TargetResponse(TargetBase):
    """Schema for serializing data sent back to the client."""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ScanJobCreate(BaseModel):
    """What the client sends to request a new scan."""

    audit_id: int
    target_id: int
    tool_name: str = Field(..., max_length=50, description="e.g., nmap, ping")


class ScanJobResponse(BaseModel):
    """What the API returns when querying a scan's status."""

    id: int
    audit_id: int
    target_id: int
    tool_name: str
    status: str
    started_at: datetime
    completed_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ScanResultResponse(BaseModel):
    id: int
    job_id: int
    raw_output: str | None = None
    parsed_data: Dict[str, Any] | None = None

    model_config = ConfigDict(from_attributes=True)
