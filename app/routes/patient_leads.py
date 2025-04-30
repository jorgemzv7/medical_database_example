from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List
from uuid import UUID
from datetime import datetime

from app.models.patient_lead import PatientLead
from app.schemas.patient_lead import (
    PatientLeadCreate,
    PatientLeadUpdate,
    PatientLeadResponse
)
from app.database import get_db

router = APIRouter(
    prefix='/api/v1/patient-leads',
    tags=['patient_leads']
)

async def invalidate_previous_active_leads(db: AsyncSession, person_id: UUID):
    """Set as inactive the previous patient leads for this person"""
    result = await db.execute(
        select(PatientLead)
        .where(and_(
            PatientLead.person_id == person_id,
            PatientLead.is_active == True
        ))
    )
    active_leads: list[PatientLead] = result.scalars().all()
    
    for lead in active_leads:
        lead.is_active = False
        lead.is_current = False
        lead.valid_to = datetime.now()
    
    if active_leads:
        await db.commit()


@router.post(
    '/',
    response_model=PatientLeadResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_patient_lead(
    patient_lead: PatientLeadCreate,
    db: AsyncSession = Depends(get_db)
):
    # Verify if there is a patient lead active with the same person_id
    result = await db.execute(
        select(PatientLead)
        .where(and_(
            PatientLead.person_id == patient_lead.person_id,
            PatientLead.is_active == True
        ))
    )
    existing_active = result.scalar_one_or_none()
    
    # Invalidate any existing active leads
    if existing_active:
        await invalidate_previous_active_leads(db, patient_lead.person_id)
    
    # Create new lead
    new_patient_lead = {
        'is_active': True,
        'valid_from': datetime.now(),
        'is_current': True,
        **patient_lead.model_dump()
    }

    try:
        db_patient_lead = PatientLead(**new_patient_lead)
        db.add(db_patient_lead)
        await db.commit()
        await db.refresh(db_patient_lead)
        return db_patient_lead
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get('/', response_model=List[PatientLeadResponse])
async def read_patient_leads(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(PatientLead)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


@router.get('/{patient_lead_id}', response_model=PatientLeadResponse)
async def read_patient_lead(
    patient_lead_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(PatientLead)
        .where(PatientLead.id == patient_lead_id)
    )
    db_patient_lead = result.scalar_one_or_none()
    
    if db_patient_lead is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Patient lead not found'
        )
    return db_patient_lead


@router.patch('/{patient_lead_id}', response_model=PatientLeadResponse)
async def update_patient_lead(
    patient_lead_id: UUID,
    patient_lead: PatientLeadUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(PatientLead)
        .where(PatientLead.id == patient_lead_id)
    )
    db_patient_lead = result.scalar_one_or_none()
    
    if db_patient_lead is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Patient lead not found'
        )
    
    update_data = patient_lead.model_dump(exclude_unset=True)
    
    # Special handling for is_active
    if 'is_active' in update_data and update_data['is_active']:
        # Check if there's another active lead for this person
        result = await db.execute(
            select(PatientLead)
            .where(and_(
                PatientLead.person_id == db_patient_lead.person_id,
                PatientLead.is_active == True,
                PatientLead.id != patient_lead_id
            ))
        )
        existing_active = result.scalar_one_or_none()
        
        if existing_active:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Cannot activate this lead. Another active lead exists for this person.'
            )
    
    # Apply updates
    for key, value in update_data.items():
        setattr(db_patient_lead, key, value)
    
    try:
        await db.commit()
        await db.refresh(db_patient_lead)
        return db_patient_lead
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete(
    '/{patient_lead_id}',
    response_model=PatientLeadResponse,
    status_code=status.HTTP_200_OK
)
async def delete_patient_lead(
    patient_lead_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(PatientLead)
        .where(PatientLead.id == patient_lead_id)
    )
    db_patient_lead: PatientLead = result.scalar_one_or_none()
    
    if db_patient_lead is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Patient lead not found'
        )
    
    # Logical delete
    db_patient_lead.is_active = False
    db_patient_lead.valid_to = datetime.now()
    
    try:
        await db.commit()
        await db.refresh(db_patient_lead)
        return db_patient_lead
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )