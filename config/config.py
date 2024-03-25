import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings: 
    APP_NAME: str = 'FastAoi Movies',
    APP_VERSION: str = '0.1.0',
    KEY_SECRET_JWT: str = os.getenv('KEY_SECRET_JWT')
    ALGORITHM_SECRET_JWT: str = os.getenv('ALGORITHM_SECRET_JWT')
    
settings = Settings()