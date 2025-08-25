from pydantic import BaseModel
from fastapi import UploadFile

class HealthCheckResult(BaseModel):
    status: str

class ConvertCSVtoSQLTableResult(BaseModel):
    status: str
    table_name: str

class CSVUploadParams(BaseModel):
    file: UploadFile

class QuerytoTableParams(BaseModel):
    nl_query: str
    file_name: str