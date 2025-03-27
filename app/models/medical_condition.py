from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base

class MedicalCondition(Base):
    __tablename__ = 'medical_conditions'
    
    condition_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    abbreviation = Column(String(10))