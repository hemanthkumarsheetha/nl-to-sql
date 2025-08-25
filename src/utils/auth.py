from typing import Callable
from functools import wraps
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from src import API_KEY


api_key_header = APIKeyHeader(name="x-api-key")

def check_x_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key"
    )

def require_api_key(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)
    
    return wrapper