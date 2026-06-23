from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Text, func
from sqlalchemy.orm import relationship
from net_sentinel.models.base import Base

class Audit(Base):
    __tablename__ = "audits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="pending", index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    scan_jobs = relationship("ScanJob", back_populates="audit", cascade="all, delete-orphan")
