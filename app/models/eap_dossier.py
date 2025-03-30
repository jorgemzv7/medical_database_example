from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base


class EAPDossier(Base):
    __tablename__ = 'eap_dossiers'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_lead_id = Column(UUID(as_uuid=True), ForeignKey('patient_leads.id'), nullable=False)
    eap_number = Column(String(32))
    product = Column(String(32))
    enrollment_date = Column(DateTime)