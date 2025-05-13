from typing import List, Optional, Dict, Any, cast
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.evidence import Evidence, EvidenceVersion, EvidenceStatus, Control
from app.schemas.evidence import EvidenceCreate, EvidenceUpdate, EvidenceVersionCreate

async def create_evidence(
    db: AsyncSession,
    *,
    obj_in: EvidenceCreate,
    created_by: int
) -> Evidence:
    db_obj = Evidence(**obj_in.model_dump())
    db_obj.created_by = created_by
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def get_evidence(
    db: AsyncSession,
    evidence_id: int
) -> Optional[Evidence]:
    result = await db.execute(
        select(Evidence)
        .options(
            selectinload(Evidence.versions),
            selectinload(Evidence.control),
            selectinload(Evidence.creator)
        )
        .where(Evidence.id == evidence_id)
    )
    return cast(Optional[Evidence], result.scalar_one_or_none())

async def get_evidence_list(
    db: AsyncSession,
    *,
    skip: int = 0,
    limit: int = 100,
    control_id: Optional[int] = None,
    status: Optional[EvidenceStatus] = None,
    evidence_type: Optional[str] = None
) -> tuple[List[Evidence], int]:
    query = select(Evidence).options(
        selectinload(Evidence.versions),
        selectinload(Evidence.control),
        selectinload(Evidence.creator)
    )
    
    if control_id:
        query = query.where(Evidence.control_id == control_id)
    if status:
        query = query.where(Evidence.status == status)
    if evidence_type:
        query = query.where(Evidence.evidence_type == evidence_type)
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)
    
    # Get paginated results
    query = query.order_by(desc(Evidence.created_at)).offset(skip).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()
    
    return items, total

async def update_evidence(
    db: AsyncSession,
    *,
    db_obj: Evidence,
    obj_in: EvidenceUpdate
) -> Evidence:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def delete_evidence(
    db: AsyncSession,
    *,
    evidence_id: int
) -> bool:
    result = await db.execute(
        select(Evidence).where(Evidence.id == evidence_id)
    )
    obj = result.scalar_one_or_none()
    if obj:
        await db.delete(obj)
        await db.commit()
        return True
    return False

async def create_evidence_version(
    db: AsyncSession,
    *,
    obj_in: EvidenceVersionCreate,
    created_by: int
) -> EvidenceVersion:
    # Get the latest version number
    result = await db.execute(
        select(func.max(EvidenceVersion.version_number))
        .where(EvidenceVersion.evidence_id == obj_in.evidence_id)
    )
    latest_version = result.scalar_one_or_none() or 0
    
    db_obj = EvidenceVersion(**obj_in.model_dump())
    db_obj.version_number = latest_version + 1
    db_obj.created_by = created_by
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def get_evidence_version(
    db: AsyncSession,
    evidence_id: int,
    version_number: int
) -> Optional[EvidenceVersion]:
    result = await db.execute(
        select(EvidenceVersion)
        .where(
            EvidenceVersion.evidence_id == evidence_id,
            EvidenceVersion.version_number == version_number
        )
    )
    return cast(Optional[EvidenceVersion], result.scalar_one_or_none())

async def update_evidence_status(
    db: AsyncSession,
    *,
    evidence_id: int,
    status: EvidenceStatus
) -> Optional[Evidence]:
    result = await db.execute(
        select(Evidence).where(Evidence.id == evidence_id)
    )
    obj = cast(Optional[Evidence], result.scalar_one_or_none())
    if obj:
        obj.status = status
        await db.commit()
        await db.refresh(obj)
        return obj
    return None

async def add_llm_analysis(
    db: AsyncSession,
    *,
    evidence_id: int,
    analysis: Dict[str, Any]
) -> Optional[Evidence]:
    result = await db.execute(
        select(Evidence).where(Evidence.id == evidence_id)
    )
    obj = cast(Optional[Evidence], result.scalar_one_or_none())
    if obj:
        obj.llm_analysis = analysis
        await db.commit()
        await db.refresh(obj)
        return obj
    return None

async def get_control(
    db: AsyncSession,
    control_id: int
) -> Optional[Control]:
    """
    Get a control by ID.
    """
    result = await db.execute(
        select(Control)
        .where(Control.id == control_id)
    )
    return cast(Optional[Control], result.scalar_one_or_none()) 