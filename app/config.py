from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    db_url: str = os.getenv('DB_URL') or open('/run/secrets/db_url').read()