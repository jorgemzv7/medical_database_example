from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from uuid import UUID

class PersonBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr

class PatientCreate(PersonBase):
    contact_record_id: UUID
    physician_id: UUID
    medical_condition_id: UUID
    initial_consult_date: Optional[datetime] = None
    eap_enrollment_date: Optional[datetime] = None

class PatientUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[EmailStr] = None
    medical_condition_id: Optional[UUID] = None

class PatientResponse(PersonBase):
    patient_id: UUID
    medical_condition_id: UUID
    is_active: bool
    
    class Config:
        orm_mode = True