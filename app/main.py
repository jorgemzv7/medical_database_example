from fastapi import FastAPI
from app.routes import patients
from app.database import engine, Base
from dotenv import load_dotenv
import os

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='myTomorrows CRM API',
    description='API for patient and contact management',
    version='1.0.0'
)

app.include_router(patients.router)

@app.get('/')
def root():
    return {'message': 'Welcome to myTomorrows API'}