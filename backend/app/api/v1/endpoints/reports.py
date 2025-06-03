from typing import List, Optional, Dict, Any, Union
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
import jinja2
import pdfkit
import tempfile
import os
from datetime import datetime

from app.api import deps
from app.crud import evidence as crud_evidence
from app.models.evidence import EvidenceStatus, EvidenceType
from app.models.user import User
from app.core.config import settings

router = APIRouter()

# Initialize Jinja2 environment
template_loader = jinja2.FileSystemLoader(searchpath="./app/templates")
template_env = jinja2.Environment(loader=template_loader)

async def generate_report_data(
    db: AsyncSession,
    control_id: Optional[int] = None,
    status: Optional[EvidenceStatus] = None,
    evidence_type: Optional[EvidenceType] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> Dict[str, Any]:
    """
    Generate data for the report.
    """
    # Get evidence items
    items, total = await crud_evidence.get_evidence_list(
        db=db,
        control_id=control_id,
        status=status,
        evidence_type=evidence_type
    )
    
    # Calculate statistics
    stats: Dict[str, Any] = {
        "total_evidence": total,
        "by_status": {},
        "by_type": {},
        "compliance_score": 0
    }
    
    compliant_count = 0
    for item in items:
        status_value = item.status.value if hasattr(item.status, 'value') else str(item.status)
        type_value = item.evidence_type.value if hasattr(item.evidence_type, 'value') else str(item.evidence_type)
        
        # Initialize counters if they don't exist
        if status_value not in stats["by_status"]:
            stats["by_status"][status_value] = 0
        if type_value not in stats["by_type"]:
            stats["by_type"][type_value] = 0
            
        stats["by_status"][status_value] += 1
        stats["by_type"][type_value] += 1
        
        if status_value == EvidenceStatus.APPROVED.value:
            compliant_count += 1
    
    # Calculate compliance score
    if total > 0:
        stats["compliance_score"] = (compliant_count / total) * 100
    
    return {
        "evidence_items": items,
        "statistics": stats,
        "generated_at": datetime.utcnow(),
        "filters": {
            "control_id": control_id,
            "status": status.value if status else None,
            "evidence_type": evidence_type.value if evidence_type else None,
            "date_range": {
                "start": start_date,
                "end": end_date
            }
        }
    }

@router.get("/html", response_class=HTMLResponse)
async def generate_html_report(
    db: AsyncSession = Depends(deps.get_db),
    control_id: Optional[int] = None,
    status: Optional[EvidenceStatus] = None,
    evidence_type: Optional[EvidenceType] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(deps.get_current_active_user)
) -> HTMLResponse:
    """
    Generate an HTML report of evidence and compliance status.
    """
    # Get report data
    report_data = await generate_report_data(
        db=db,
        control_id=control_id,
        status=status,
        evidence_type=evidence_type,
        start_date=start_date,
        end_date=end_date
    )
    
    # Load and render template
    template = template_env.get_template("report.html")
    html_content = template.render(
        report=report_data,
        user=current_user,
        company_name=settings.PROJECT_NAME
    )
    
    return HTMLResponse(content=html_content)

@router.get("/pdf")
async def generate_pdf_report(
    db: AsyncSession = Depends(deps.get_db),
    control_id: Optional[int] = None,
    status: Optional[EvidenceStatus] = None,
    evidence_type: Optional[EvidenceType] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(deps.get_current_active_user)
) -> FileResponse:
    """
    Generate a PDF report of evidence and compliance status.
    """
    # Get report data
    report_data = await generate_report_data(
        db=db,
        control_id=control_id,
        status=status,
        evidence_type=evidence_type,
        start_date=start_date,
        end_date=end_date
    )
    
    # Load and render template
    template = template_env.get_template("report.html")
    html_content = template.render(
        report=report_data,
        user=current_user,
        company_name=settings.PROJECT_NAME
    )
    
    # Create temporary files
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as html_file:
        html_file.write(html_content.encode())
        html_path = html_file.name
    
    pdf_path = html_path.replace(".html", ".pdf")
    
    try:
        # Convert HTML to PDF
        pdfkit.from_file(
            html_path,
            pdf_path,
            options={
                "page-size": "A4",
                "margin-top": "20mm",
                "margin-right": "20mm",
                "margin-bottom": "20mm",
                "margin-left": "20mm",
                "encoding": "UTF-8",
                "no-outline": None
            }
        )
        
        # Return PDF file
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"compliance_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
    finally:
        # Clean up temporary files
        os.unlink(html_path)
        if os.path.exists(pdf_path):
            os.unlink(pdf_path)

@router.get("/summary", response_model=Dict[str, Any])
async def get_report_summary(
    db: AsyncSession = Depends(deps.get_db),
    control_id: Optional[int] = None,
    status: Optional[EvidenceStatus] = None,
    evidence_type: Optional[EvidenceType] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(deps.get_current_active_user)
) -> Dict[str, Any]:
    """
    Get a summary of the report data without generating the full report.
    """
    report_data = await generate_report_data(
        db=db,
        control_id=control_id,
        status=status,
        evidence_type=evidence_type,
        start_date=start_date,
        end_date=end_date
    )
    
    return {
        "statistics": report_data["statistics"],
        "generated_at": report_data["generated_at"],
        "filters": report_data["filters"]
    } 