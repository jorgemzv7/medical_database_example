from fastapi import FastAPI
from app.routes import patient_leads
from app.database import engine, Base
from dotenv import load_dotenv

load_dotenv()

async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield

    # Shutdown
    await engine.dispose()


app = FastAPI(
    title='myTomorrows CRM API',
    description='API for patient and contact management',
    version='1.0.0',
    lifespan=lifespan
)


app.include_router(patient_leads.router)

@app.get('/')
def root():
    return {'message': 'Welcome to myTomorrows API'}