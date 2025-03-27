from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from app.models.person import Person

class Contact(Person):
    __tablename__ = 'contacts'
    
    contact_id = Column(UUID(as_uuid=True), ForeignKey('persons.person_id'), primary_key=True)
    contact_type = Column(String(20))  # patient-lead, physician, pharmacist
    job_title = Column(String(50))
    hospital_id = Column(UUID(as_uuid=True), ForeignKey('hospitals.hospital_id'))
    medical_license_number = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'contact'
    }