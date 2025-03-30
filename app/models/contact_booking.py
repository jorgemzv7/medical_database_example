from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base


class ContactBooking(Base):
    __tablename__ = 'contact_bookings'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_lead_id = Column(UUID(as_uuid=True), ForeignKey('patient_leads.id'), nullable=False)
    date = Column(DateTime, nullable=False)
    reminder = Column(DateTime, nullable=False)

