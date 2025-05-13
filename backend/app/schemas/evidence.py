from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

from app.models.evidence import EvidenceStatus, EvidenceType

class EvidenceBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    evidence_type: EvidenceType
    control_id: int
    content: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None
    expires_at: Optional[datetime] = None

class EvidenceCreate(EvidenceBase):
    pass

class EvidenceUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[EvidenceStatus] = None
    content: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    expires_at: Optional[datetime] = None
    llm_analysis: Optional[Dict[str, Any]] = None

class EvidenceVersionBase(BaseModel):
    content: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None
    comment: Optional[str] = None

class EvidenceVersionCreate(EvidenceVersionBase):
    evidence_id: int

class EvidenceVersionInDB(EvidenceVersionBase):
    id: int
    evidence_id: int
    version_number: int
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True

class EvidenceInDB(EvidenceBase):
    id: int
    status: EvidenceStatus
    created_by: int
    created_at: datetime
    updated_at: datetime
    llm_analysis: Optional[Dict[str, Any]] = None
    versions: List[EvidenceVersionInDB] = []

    class Config:
        from_attributes = True

class EvidenceWithRelations(EvidenceInDB):
    control_title: str
    creator_email: str

    class Config:
        from_attributes = True

class EvidenceList(BaseModel):
    items: List[EvidenceWithRelations]
    total: int
    page: int
    size: int
    pages: int 