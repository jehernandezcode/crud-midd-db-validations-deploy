from jwt import encode, decode
from config.config import settings

key = settings.KEY_SECRET_JWT
algorithm = settings.ALGORITHM_SECRET_JWT

def create_token(data: dict) -> str:
    token :str = encode(payload=data, key=key, algorithm=algorithm)
    return token

def validate_token(token : str) -> dict:
    data: dict = decode(token, key=key, algorithms=[algorithm])
    return data