# The specific asset, device, IP address, or subnet that we are targeting
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from net_sentinel.models.base import Base


class Target(Base):
    __tablename__ = "targets"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String(45), nullable=False, index=True)
    hostname = Column(String(255), nullable=True)
    mac_address = Column(String(17), nullable=True)
    label = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    scan_jobs = relationship(
        "ScanJob", back_populates="target", cascade="all, delete-orphan"
    )


class ScanJob(Base):
    __tablename__ = "scanjobs"

    id = Column(Integer, primary_key=True, index=True)
    audit_id = Column(
        Integer, ForeignKey("audits.id", ondelete="CASCADE"), nullable=False, index=True
    )
    target_id = Column(
        Integer,
        ForeignKey("targets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    tool_name = Column(String(50), nullable=False)
    status = Column(String(20), default="pending", index=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    audit = relationship("Audit", back_populates="scan_jobs")
    target = relationship("Target", back_populates="scan_jobs")
    result = relationship(
        "ScanResult", back_populates="job", uselist=False, cascade="all, delete-orphan"
    )


class ScanResult(Base):
    __tablename__ = "scanresults"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(
        Integer,
        ForeignKey("scanjobs.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    raw_output = Column(Text, nullable=True)
    parsed_data = Column(JSON, nullable=True)

    job = relationship("ScanJob", back_populates="result")
