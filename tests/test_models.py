from app.models.patient import Patient
from app.models.contact import Contact
from app.models.medical_condition import MedicalCondition
from sqlalchemy.exc import IntegrityError
import pytest

def test_create_patient(db):
    # Create medical condition and physician
    condition = MedicalCondition(name='Spanish flu', abbreviation='SPF')
    contact = Contact(
        firstname='Dr. Samuel',
        lastname='Giffard',
        email='dr.giffard@myt.com',
        contact_type='physician'
    )
    db.add_all([condition, contact])
    db.commit()

    # Create patient
    patient = Patient(
        firstname='John',
        lastname='Doe',
        email='john.doe@example.com',
        contact_record_id=contact.contact_id,
        physician_id=contact.contact_id,
        medical_condition_id=condition.condition_id
    )
    db.add(patient)
    db.commit()

    # Verificar
    assert patient.patient_id is not None
    assert patient.medical_condition.name == 'Duchenne'


def test_email_uniqueness(db):
    """
    Test that two patients cannot have the same email address
    """
    patient1 = Patient(
        firstname='John',
        lastname='Doe',
        email='duplicate@example.com',
        contact_record_id=None,
        physician_id=None,
        medical_condition_id=None
    )
    db.add(patient1)
    db.commit()

    with pytest.raises(IntegrityError):
        patient2 = Patient(
            firstname='Jane',
            lastname='Doe',
            email='duplicate@example.com',
            contact_record_id=None,
            physician_id=None,
            medical_condition_id=None
        )
        db.add(patient2)
        db.commit()