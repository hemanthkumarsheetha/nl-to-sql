import os
from fastapi import APIRouter, UploadFile, File
from models.api_models import QuerytoTableParams, CSVUploadParams
from src.services.ingest.create_tables import ingest_csv_to_database
from src.services.query.nltosql import craft_a_response
from src.utils.auth import require_api_key

router = APIRouter(prefix="/api/v1/text-to-sql", tags=["query"])


@router.post("/ingest-csv-to-sql")
@require_api_key
async def ingest_csv_file_to_sql(params: CSVUploadParams):
    async def read_file(file: UploadFile):
        content = await file.read()
        os.makedirs("/tmp/",exist_ok=True)
        file_path = f"/tmp/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(content)
        return file_path

    file_path = await read_file(params.file)
    result = ingest_csv_to_database(file_path)
    return result


@router.post("/query-table-with-filter")
@require_api_key
async def query_table(params: QuerytoTableParams):
    final_response = craft_a_response(params.nl_query, params.file_name)
    return final_response
