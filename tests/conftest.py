from uuid import uuid4
import pytest_asyncio
from fastapi.testclient import TestClient  # Change this import
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.models.person import Person
from app.models.hospital import Hospital
from app.models.medical_condition import MedicalCondition
from app.models.physician import Physician
from app.models.patient_lead import PatientLead
from app.models.contact_booking import ContactBooking
from app.models.referal import Referal
from app.models.eap_dossier import EAPDossier
from app.database import Base, get_db

TEST_DATABASE_URL = 'postgresql+asyncpg://testuser:testpass@test-db:5432/testdb'

@pytest_asyncio.fixture
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest_asyncio.fixture
async def session(engine):
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        yield session

@pytest_asyncio.fixture
async def client(session: AsyncSession):
    async def override_get_db():
        yield session
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest_asyncio.fixture
async def sample_physician(session: AsyncSession):
    physician = Physician(
        id=uuid4(),
        firstname="Doctor",
        lastname="Who",
        license_number=f"MD-{uuid4()}"
    )
    session.add(physician)
    await session.commit()
    return physician