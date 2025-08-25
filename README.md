# Text-to-SQL API

A FastAPI application for converting natural language queries to SQL and ingesting CSV files into SQL tables.

## Installation

Install dependencies using uv:

```bash
uv sync
```

## Configuration

Before running the application, you need to add your credentials in `src/__init__.py`:

```python
# API Configuration
CONN_STRING="<postgresql-table-conn-string>"
GOOGLE_API_KEY="<google-api-key>"
API_KEY="<api-key>"
```

## Database Setup

### Create TableMetaData Table

Before using the API, you need to create the `TableMetaData` table in your PostgreSQL database. This table stores metadata about ingested CSV files and their associated prompts.

You can create the table by running the following SQL:

```sql
CREATE TABLE "table-meta-data" (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(255) NOT NULL,
    prompt TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

Alternatively, you can uncomment the following lines in `src/db/models.py` and run the application once to automatically create the table:

```python
# Uncomment these lines in src/db/models.py
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
```

## Running the API

Start the FastAPI server:

```bash
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Ingest CSV to SQL

Upload a CSV file to create a SQL table and generate a prompt specific to the file:

```bash
curl -X POST "http://localhost:8000/api/v1/text-to-sql/ingest-csv-to-sql" \
  -H "X-API-Key: your-api-key" \
  -F "file=@your-file.csv"
```

Response:
```json
{
  "status": "success",
  "table_name": "generated_table_name"
}
```

### Query Table with Natural Language

Query existing tables using natural language:

```bash
curl -X POST "http://localhost:8000/api/v1/text-to-sql/query-table-with-filter" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "nl_query": "Show me all records where age is greater than 25",
    "file_name": "your-table-name"
  }'
```

Response:
```json
"SELECT * FROM your_table_name WHERE age > 25"

```

## API Documentation

Once the server is running, you can view the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`