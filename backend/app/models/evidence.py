from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text, Enum
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base

class EvidenceStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"

class EvidenceType(str, enum.Enum):
    DOCUMENT = "document"
    SCREENSHOT = "screenshot"
    AWS_CONFIG = "aws_config"
    AWS_CLI = "aws_cli"
    MANUAL = "manual"

class Control(Base):
    __tablename__ = "control"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    framework = Column(String(100), nullable=False)  # e.g., "NIST", "ISO27001", "SOC2"
    control_id = Column(String(50), nullable=False)  # e.g., "NIST-AC-1", "ISO-5.1.1"
    category = Column(String(100), nullable=True)  # e.g., "Access Control", "Security"
    requirements = Column(JSON, nullable=True)  # Detailed requirements as JSON
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    evidence = relationship("Evidence", back_populates="control")

class Evidence(Base):
    __tablename__ = "evidence"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    evidence_type = Column(Enum(EvidenceType), nullable=False)
    status = Column(Enum(EvidenceStatus), default=EvidenceStatus.PENDING)
    content = Column(JSON, nullable=False)  # Stores the actual evidence data
    metadata = Column(JSON, nullable=True)  # Additional metadata like AWS region, resource ARN, etc.
    control_id = Column(Integer, ForeignKey("control.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    llm_analysis = Column(JSON, nullable=True)  # Stores LLM analysis of the evidence
    
    # Relationships
    control = relationship("Control", back_populates="evidence")
    creator = relationship("User", back_populates="evidence")
    versions = relationship("EvidenceVersion", back_populates="evidence", cascade="all, delete-orphan")

class EvidenceVersion(Base):
    __tablename__ = "evidence_version"
    
    id = Column(Integer, primary_key=True, index=True)
    evidence_id = Column(Integer, ForeignKey("evidence.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    content = Column(JSON, nullable=False)
    metadata = Column(JSON, nullable=True)
    created_by = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    comment = Column(Text, nullable=True)
    
    # Relationships
    evidence = relationship("Evidence", back_populates="versions")
    creator = relationship("User", back_populates="evidence_versions") 