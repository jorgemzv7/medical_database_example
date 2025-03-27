from pydantic import BaseSettings, PostgresDsn

class Settings(BaseSettings):
    db_url: PostgresDsn  # Valida formato PostgreSQL
    app_env: str = 'production'
    debug: bool = False
    secret_key: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()