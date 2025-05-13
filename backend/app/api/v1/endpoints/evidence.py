from typing import List, Optional, Dict, Any, cast
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.status import HTTP_404_NOT_FOUND
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.crud import evidence as crud_evidence
from app.schemas.evidence import (
    EvidenceCreate,
    EvidenceUpdate,
    EvidenceInDB,
    EvidenceList,
    EvidenceVersionCreate,
    EvidenceVersionInDB,
    EvidenceWithRelations
)
from app.models.evidence import EvidenceStatus, EvidenceType
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=EvidenceInDB)
async def create_evidence(
    *,
    db: AsyncSession = Depends(deps.get_db),
    evidence_in: EvidenceCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> EvidenceInDB:
    """
    Create new evidence.
    """
    evidence = await crud_evidence.create_evidence(
        db=db,
        obj_in=evidence_in,
        created_by=current_user.id
    )
    return cast(EvidenceInDB, EvidenceInDB.model_validate(evidence))

@router.get("/", response_model=EvidenceList)
async def list_evidence(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    control_id: Optional[int] = None,
    status: Optional[EvidenceStatus] = None,
    evidence_type: Optional[EvidenceType] = None,
    current_user: User = Depends(deps.get_current_active_user)
) -> EvidenceList:
    """
    Retrieve evidence items with pagination and filtering.
    """
    items, total = await crud_evidence.get_evidence_list(
        db=db,
        skip=skip,
        limit=limit,
        control_id=control_id,
        status=status,
        evidence_type=evidence_type
    )
    
    # Convert to response model with relations
    evidence_items = []
    for item in items:
        evidence_items.append(
            EvidenceWithRelations(
                **item.__dict__,
                control_title=item.control.title,
                creator_email=item.creator.email
            )
        )
    
    return EvidenceList(
        items=evidence_items,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )

@router.get("/{evidence_id}", response_model=EvidenceWithRelations)
async def get_evidence(
    evidence_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> EvidenceWithRelations:
    """
    Get evidence by ID.
    """
    evidence = await crud_evidence.get_evidence(db=db, evidence_id=evidence_id)
    if not evidence:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Evidence not found"
        )
    return EvidenceWithRelations(
        **evidence.__dict__,
        control_title=evidence.control.title,
        creator_email=evidence.creator.email
    )

@router.put("/{evidence_id}", response_model=EvidenceInDB)
async def update_evidence(
    *,
    db: AsyncSession = Depends(deps.get_db),
    evidence_id: int,
    evidence_in: EvidenceUpdate,
    current_user: User = Depends(deps.get_current_active_user)
) -> EvidenceInDB:
    """
    Update evidence.
    """
    evidence = await crud_evidence.get_evidence(db=db, evidence_id=evidence_id)
    if not evidence:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Evidence not found"
        )
    evidence = await crud_evidence.update_evidence(
        db=db,
        db_obj=evidence,
        obj_in=evidence_in
    )
    return cast(EvidenceInDB, EvidenceInDB.model_validate(evidence))

@router.delete("/{evidence_id}", response_model=bool)
async def delete_evidence(
    *,
    db: AsyncSession = Depends(deps.get_db),
    evidence_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> bool:
    """
    Delete evidence.
    """
    evidence = await crud_evidence.get_evidence(db=db, evidence_id=evidence_id)
    if not evidence:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Evidence not found"
        )
    return await crud_evidence.delete_evidence(db=db, evidence_id=evidence_id)

@router.post("/{evidence_id}/versions", response_model=EvidenceVersionInDB)
async def create_evidence_version(
    *,
    db: AsyncSession = Depends(deps.get_db),
    evidence_id: int,
    version_in: EvidenceVersionCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> EvidenceVersionInDB:
    """
    Create a new version of evidence.
    """
    evidence = await crud_evidence.get_evidence(db=db, evidence_id=evidence_id)
    if not evidence:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Evidence not found"
        )
    version = await crud_evidence.create_evidence_version(
        db=db,
        obj_in=version_in,
        created_by=current_user.id
    )
    return cast(EvidenceVersionInDB, EvidenceVersionInDB.model_validate(version))

@router.get("/{evidence_id}/versions/{version_number}", response_model=EvidenceVersionInDB)
async def get_evidence_version(
    evidence_id: int,
    version_number: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> EvidenceVersionInDB:
    """
    Get a specific version of evidence.
    """
    version = await crud_evidence.get_evidence_version(
        db=db,
        evidence_id=evidence_id,
        version_number=version_number
    )
    if not version:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Evidence version not found"
        )
    return cast(EvidenceVersionInDB, EvidenceVersionInDB.model_validate(version))

@router.put("/{evidence_id}/status", response_model=EvidenceInDB)
async def update_evidence_status(
    *,
    db: AsyncSession = Depends(deps.get_db),
    evidence_id: int,
    status: EvidenceStatus,
    current_user: User = Depends(deps.get_current_active_user)
) -> EvidenceInDB:
    """
    Update evidence status.
    """
    evidence = await crud_evidence.update_evidence_status(
        db=db,
        evidence_id=evidence_id,
        status=status
    )
    if not evidence:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Evidence not found"
        )
    return cast(EvidenceInDB, EvidenceInDB.model_validate(evidence)) 