from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate, PatientResponse
from app.database import get_db

router = APIRouter(
    prefix='/patients',
    tags=['patients'],
    responses={404: {'description': 'Not found'}},
)



@router.post('/', response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    """
    Create a new patient record.
    
    - **firstname**: Patient's first name
    - **lastname**: Patient's last name
    - **email**: Patient's email (must be unique)
    - **contact_record_id**: ID of the related Contact record
    - **physician_id**: ID of the assigned physician (Contact)
    - **medical_condition_id**: ID of the medical condition
    """
    # Check if email already exists
    db_patient = db.query(Patient).filter(Patient.email == patient.email).first()
    if db_patient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already registered'
        )
    
    new_patient = Patient(**patient.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient


@router.get('/', response_model=List[PatientResponse])
def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of patients with pagination.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    """
    patients = db.query(Patient).offset(skip).limit(limit).all()
    return patients


@router.get('/{patient_id}', response_model=PatientResponse)
def read_patient(patient_id: str, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific patient.
    
    - **patient_id**: UUID of the patient to retrieve
    """
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Patient not found'
        )
    return patient


@router.put('/{patient_id}', response_model=PatientResponse)
def update_patient(
    patient_id: str, 
    patient_update: PatientUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update a patient's information.
    
    - **patient_id**: UUID of the patient to update
    - **All fields are optional** - only provided fields will be updated
    """
    db_patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not db_patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Patient not found'
        )
    
    update_data = patient_update.dict(exclude_unset=True)
    
    # Prevent email duplication
    if 'email' in update_data:
        existing_patient = db.query(Patient).filter(
            Patient.email == update_data['email'],
            Patient.patient_id != patient_id
        ).first()
        if existing_patient:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email already in use by another patient'
            )
    
    for field, value in update_data.items():
        setattr(db_patient, field, value)
    
    db.commit()
    db.refresh(db_patient)
    return db_patient


@router.delete('/{patient_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    """
    Delete a patient record (soft delete implementation).
    
    - **patient_id**: UUID of the patient to deactivate
    """
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Patient not found'
        )
    
    # Soft delete (update is_active flag)
    patient.is_active = False
    db.commit()
    return {'ok': True}