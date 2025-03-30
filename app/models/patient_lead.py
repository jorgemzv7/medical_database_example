from sqlalchemy import Column, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class PatientLead(Base):
    __tablename__ = 'patient_leads'
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    person_id = Column(UUID(as_uuid=True), ForeignKey('persons.id'), nullable=False)
    medical_condition_id = Column(UUID(as_uuid=True), ForeignKey('medical_conditions.id'))
    physician_id = Column(UUID(as_uuid=True), ForeignKey('physicians.id'))
    is_active = Column(Boolean, default=True)  # soft-delete
    valid_from = Column(DateTime, nullable=False) # Initial consult record now
    valid_to = Column(DateTime, nullable=True)
    is_current = Column(Boolean, default=True)  # current record
