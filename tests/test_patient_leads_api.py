import pytest
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.models.patient_lead import PatientLead
from app.models.person import Person, PersonRole
from app.models.medical_condition import MedicalCondition

@pytest.mark.asyncio
async def test_create_patient_lead(session: AsyncSession):
    # First we create a valid Person and a valid MedicalCondition
    person = Person(
        id=uuid4(),
        firstname='John',
        lastname='Doe',
        email='john.doe@example.com',
        job_title='Patient',
        created_at=datetime.now(),
        type=PersonRole.PATIENT
    )
    
    medical_condition = MedicalCondition(id=uuid4(), name='Test Condition')
    
    session.add_all([person, medical_condition])
    await session.commit()
    
    lead = PatientLead(
        person_id=person.id,
        medical_condition_id=medical_condition.id,
        is_active=True,
        is_current=True,
        valid_from=datetime.now()
    )
    
    session.add(lead)
    await session.commit()
    
    assert lead.id is not None
    assert lead.valid_to is None

@pytest.mark.asyncio
async def test_unique_constraints(session: AsyncSession):
    # First we create a Person and two valid MedicalConditions
    person = Person(
        id=uuid4(),
        firstname='Jane',
        lastname='Smith',
        email='jane.smith@example.com',
        job_title='Patient',
        created_at=datetime.now(),
        type=PersonRole.PATIENT
    )
    
    condition1 = MedicalCondition(id=uuid4(), name='Condition 1')
    condition2 = MedicalCondition(id=uuid4(), name='Condition 2')
    
    session.add_all([person, condition1, condition2])
    await session.commit()
    
    # First lead
    lead1 = PatientLead(
        person_id=person.id,
        medical_condition_id=condition1.id,
        is_active=True,
        is_current=True,
        valid_from=datetime.now()
    )
    session.add(lead1)
    await session.commit()
    
    # Second lead with the same person but different condition
    lead2 = PatientLead(
        person_id=person.id,
        medical_condition_id=condition2.id,
        is_active=True,
        is_current=True,
        valid_from=datetime.now()
    )
    session.add(lead2)
    
    # Should fail because of the single constraint (assuming you have a constraint that prevents multiple active leads).
    with pytest.raises(IntegrityError):
        await session.commit()
    
    await session.rollback()

