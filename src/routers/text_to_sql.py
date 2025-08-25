import os
from fastapi import APIRouter, UploadFile, File
from models.api_models import ConvertCSVtoSQLTableResult
from src.services.text_to_sql.create_tables import ingest_csv_to_database
from src.utils.auth import require_api_key

router = APIRouter(prefix="/api/v1/text-to-sql", tags=["query"])

async def read_file(file: UploadFile):
    content = await file.read()
    os.makedirs("/tmp/",exist_ok=True)
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(content)
    return file_path

@router.post("/ingest-csv-to-sql")
@require_api_key
async def ingest_csv_file_to_sql(file: UploadFile = File()):
    file_path = await read_file(file)
    result = ingest_csv_to_database(file_path)
    return result