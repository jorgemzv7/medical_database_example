from fastapi import FastAPI
from app.routes import patient_leads, physicians, persons
from app.database import engine, Base
from dotenv import load_dotenv
from app.models.person import Person
from app.models.hospital import Hospital
from app.models.physician import Physician
from app.models.contact_booking import ContactBooking
from app.models.eap_dossier import EAPDossier
from app.models.medical_condition import MedicalCondition
from app.models.patient_lead import PatientLead
from app.models.referal import Referal


Base.metadata.create_all(bind=engine)

load_dotenv()
app = FastAPI(
    title='myTomorrows CRM API',
    description='API for patient and contact management',
    version='1.0.0'
)

app.include_router(persons.router)
app.include_router(patient_leads.router)
app.include_router(physicians.router)

@app.get('/')
def root():
    return {'message': 'Welcome to myTomorrows API'}