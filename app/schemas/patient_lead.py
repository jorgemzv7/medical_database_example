from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class PatientLeadBase(BaseModel):
    person_id: UUID
    medical_condition_id: UUID
    physician_id: Optional[UUID] = None
    is_active: bool = True
    valid_from: datetime
    valid_to: Optional[datetime] = None
    is_current: bool = True

class PatientLeadCreate(BaseModel):
    person_id: UUID
    medical_condition_id: UUID
    physician_id: Optional[UUID] = None


class PatientLeadUpdate(BaseModel):
    medical_condition_id: Optional[UUID] = None
    physician_id: Optional[UUID] = None
    is_active: Optional[bool] = None
    is_current: Optional[bool] = None

class PatientLeadResponse(PatientLeadBase):
    id: UUID

    class Config:
        from_attributes = True