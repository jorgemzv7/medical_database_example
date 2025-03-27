from sqlalchemy import Column, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.models.person import Person

class Patient(Person):
    __tablename__ = 'patients'
    
    patient_id = Column(UUID(as_uuid=True), ForeignKey('persons.person_id'), primary_key=True)
    contact_record_id = Column(UUID(as_uuid=True), ForeignKey('contacts.contact_id'))
    physician_id = Column(UUID(as_uuid=True), ForeignKey('contacts.contact_id'))
    medical_condition_id = Column(UUID(as_uuid=True), ForeignKey('medical_conditions.condition_id'))
    initial_consult_date = Column(DateTime)
    eap_enrollment_date = Column(DateTime)
    is_active = Column(Boolean, default=True)  # soft-delete

    __mapper_args__ = {
        'polymorphic_identity': 'patient'
    }