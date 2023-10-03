
from pydantic import BaseSettings
import os
class Settings(BaseSettings):
    SERVER_DOMAIN: str = 'ariksa.io'
    API_V1_STR = 'v1'


settings = Settings()
