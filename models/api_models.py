from pydantic import BaseModel
from fastapi import UploadFile

class HealthCheckResult(BaseModel):
    status: str

class ConvertCSVtoSQLTableResult(BaseModel):
    status: str
    table_name: str