from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.models.user import User
from app.models.program import Program
from app.dependencies.auth import get_current_active_user
from app.schemas.program import ProgramResponse, ProgramCreate, ProgramUpdate, ProgramRecommendation

router = APIRouter()


@router.get("/", response_model=List[ProgramResponse])
async def list_programs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    search: Optional[str] = None,
    degree_type: Optional[str] = None,
    location: Optional[str] = None,
    min_deadline: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get list of programs with optional filters"""
    query = select(Program)
    
    # Apply filters
    conditions = []
    if search:
        search_term = f"%{search}%"
        conditions.append(
            or_(
                Program.university.ilike(search_term),
                Program.program_name.ilike(search_term),
                Program.description.ilike(search_term)
            )
        )
    
    if degree_type:
        conditions.append(Program.degree_type == degree_type)
    
    if location:
        conditions.append(Program.location.ilike(f"%{location}%"))
    
    if min_deadline:
        conditions.append(Program.deadline >= min_deadline)
    
    if conditions:
        query = query.where(and_(*conditions))
    
    query = query.offset(skip).limit(limit).order_by(Program.deadline.asc())
    
    result = await db.execute(query)
    programs = result.scalars().all()
    
    return programs


@router.get("/{program_id}", response_model=ProgramResponse)
async def get_program(
    program_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get specific program by ID"""
    result = await db.execute(
        select(Program).where(Program.id == program_id)
    )
    program = result.scalar_one_or_none()
    
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    return program


@router.post("/", response_model=ProgramResponse, status_code=201)
async def create_program(
    program_data: ProgramCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new program (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create programs")
    
    program = Program(**program_data.model_dump())
    db.add(program)
    await db.commit()
    await db.refresh(program)
    
    return program


@router.patch("/{program_id}", response_model=ProgramResponse)
async def update_program(
    program_id: int,
    program_data: ProgramUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update program (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update programs")
    
    result = await db.execute(
        select(Program).where(Program.id == program_id)
    )
    program = result.scalar_one_or_none()
    
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    # Update fields
    update_data = program_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(program, field, value)
    
    await db.commit()
    await db.refresh(program)
    
    return program


@router.delete("/{program_id}", status_code=204)
async def delete_program(
    program_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete program (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete programs")
    
    result = await db.execute(
        select(Program).where(Program.id == program_id)
    )
    program = result.scalar_one_or_none()
    
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    await db.delete(program)
    await db.commit()
    
    return None


@router.get("/recommendations/ai", response_model=List[ProgramRecommendation])
async def get_ai_recommendations(
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get AI-powered program recommendations based on user profile"""
    # TODO: Implement AI matching logic with OpenAI
    # For now, return programs ordered by average match score
    
    result = await db.execute(
        select(Program)
        .order_by(Program.average_match_score.desc().nullslast())
        .limit(limit)
    )
    programs = result.scalars().all()
    
    recommendations = [
        ProgramRecommendation(
            program=program,
            match_score=program.average_match_score or 0.0,
            match_reasons=["Profile match", "Academic fit", "Location preference"]
        )
        for program in programs
    ]
    
    return recommendations
