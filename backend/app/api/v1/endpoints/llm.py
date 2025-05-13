from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import openai
from openai import AsyncOpenAI

from app.api import deps
from app.core.config import settings
from app.crud import evidence as crud_evidence
from app.models.evidence import Evidence, EvidenceType
from app.models.user import User

router = APIRouter()
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def analyze_evidence_with_llm(evidence: Evidence) -> Dict[str, Any]:
    """
    Analyze evidence using OpenAI's GPT model.
    """
    if not settings.OPENAI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenAI API key not configured"
        )

    # Prepare the prompt based on evidence type
    prompt = f"""
    Analyze the following compliance evidence and provide:
    1. A summary of the evidence
    2. Compliance assessment
    3. Potential risks or issues
    4. Recommended remediation steps if needed
    
    Evidence Type: {evidence.evidence_type}
    Control: {evidence.control.title}
    Content: {evidence.content}
    Metadata: {evidence.metadata}
    """

    try:
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are a compliance expert specializing in AWS security and compliance frameworks. Analyze the provided evidence and provide detailed insights."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        analysis = response.choices[0].message.content
        
        # Structure the analysis
        return {
            "summary": analysis,
            "compliance_status": "compliant" if "compliant" in analysis.lower() else "non-compliant",
            "risks": [line.strip() for line in analysis.split("\n") if "risk" in line.lower()],
            "remediation_steps": [line.strip() for line in analysis.split("\n") if "remediation" in line.lower() or "recommend" in line.lower()],
            "raw_analysis": analysis
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing evidence: {str(e)}"
        )

@router.post("/analyze/{evidence_id}", response_model=Dict[str, Any])
async def analyze_evidence(
    evidence_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Dict[str, Any]:
    """
    Analyze evidence using LLM and store the analysis.
    """
    evidence = await crud_evidence.get_evidence(db=db, evidence_id=evidence_id)
    if not evidence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidence not found"
        )
    
    analysis = await analyze_evidence_with_llm(evidence)
    
    # Store the analysis
    evidence = await crud_evidence.add_llm_analysis(
        db=db,
        evidence_id=evidence_id,
        analysis=analysis
    )
    
    return analysis

@router.post("/suggest-remediation/{evidence_id}", response_model=Dict[str, Any])
async def suggest_remediation(
    evidence_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Dict[str, Any]:
    """
    Get detailed remediation suggestions for non-compliant evidence.
    """
    evidence = await crud_evidence.get_evidence(db=db, evidence_id=evidence_id)
    if not evidence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidence not found"
        )
    
    if not settings.OPENAI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenAI API key not configured"
        )

    prompt = f"""
    Provide detailed remediation steps for the following non-compliant evidence:
    
    Evidence Type: {evidence.evidence_type}
    Control: {evidence.control.title}
    Content: {evidence.content}
    Metadata: {evidence.metadata}
    
    Include:
    1. Step-by-step remediation instructions
    2. AWS CLI commands or console steps
    3. Expected outcome after remediation
    4. Verification steps
    """

    try:
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AWS security expert. Provide detailed, actionable remediation steps for non-compliant resources."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=1500
        )
        
        remediation = response.choices[0].message.content
        
        return {
            "remediation_steps": remediation,
            "aws_commands": [line.strip() for line in remediation.split("\n") if "aws " in line.lower()],
            "verification_steps": [line.strip() for line in remediation.split("\n") if "verify" in line.lower() or "check" in line.lower()],
            "raw_remediation": remediation
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating remediation: {str(e)}"
        )

@router.post("/explain-control/{control_id}", response_model=Dict[str, Any])
async def explain_control(
    control_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Dict[str, Any]:
    """
    Get a detailed explanation of a control and its requirements.
    """
    # Get control details from the database
    control = await crud_evidence.get_control(db=db, control_id=control_id)
    if not control:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Control not found"
        )
    
    if not settings.OPENAI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenAI API key not configured"
        )

    prompt = f"""
    Explain the following compliance control in detail:
    
    Control: {control.title}
    Description: {control.description}
    Framework: {control.framework}
    
    Include:
    1. Purpose and importance
    2. Key requirements
    3. Common implementation approaches in AWS
    4. Best practices
    5. Common pitfalls to avoid
    """

    try:
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are a compliance expert. Explain controls in a clear, detailed manner with practical implementation guidance."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=1500
        )
        
        explanation = response.choices[0].message.content
        
        return {
            "explanation": explanation,
            "key_points": [line.strip() for line in explanation.split("\n") if line.strip() and not line.startswith(("1.", "2.", "3.", "4.", "5."))],
            "best_practices": [line.strip() for line in explanation.split("\n") if "best practice" in line.lower()],
            "common_pitfalls": [line.strip() for line in explanation.split("\n") if "pitfall" in line.lower() or "avoid" in line.lower()],
            "raw_explanation": explanation
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error explaining control: {str(e)}"
        ) 