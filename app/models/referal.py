from sqlalchemy import Column, DateTime, ForeignKey, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum as PythonEnum
import uuid
from app.database import Base


class ReferalType(PythonEnum):
    CT = "CT"
    EAP = "EAP"


class Referal(Base):
    __tablename__ = 'referals'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_lead_id = Column(UUID(as_uuid=True), ForeignKey('patient_leads.id'), nullable=False)
    type = Column(Enum(ReferalType), nullable=False)
    created_at = Column(DateTime, nullable=False)
    start_datetime = Column(DateTime, nullable=False)
    outcome = Column(String(32))

