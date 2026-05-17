from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    google_api_key: str
    database_hostname:str
    database_port:str
    database_password:str
    database_name:str
    database_username:str
    pinecone_api_key:str
    class Config:
        env_file = ".env"

settings = Settings()
