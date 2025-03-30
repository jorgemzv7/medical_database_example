from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base



class Physician(Base):
    __tablename__ = 'physicians'
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    person_id = Column(UUID(as_uuid=True), ForeignKey('persons.id'), nullable=False)
    hospital_id = Column(UUID(as_uuid=True), ForeignKey('hospitals.id'), nullable=True) # ? Add physicians without hospital
    medical_licence_number = Column(String(32), unique=True, nullable=False)
    specialization = Column(String(50), nullable=True)
