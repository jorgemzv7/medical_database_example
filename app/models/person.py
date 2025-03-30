from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from enum import Enum as PythonEnum
from app.database import Base

class PersonRole(PythonEnum):
    PATIENT = "patient"
    PHYSICIAN = "physician"
    PHARMACIST = "pharmacist"
    PATIENT_NAVIGATOR = "patient_navigator"

class Person(Base):
    __tablename__ = 'persons'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    job_title = Column(String(50))
    created_at = Column(DateTime, nullable=False)
    type = Column(Enum(PersonRole), nullable=False)
 