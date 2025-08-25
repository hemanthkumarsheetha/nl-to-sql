import pandas as pd
from sqlalchemy import create_engine, MetaData, Table
from src.utils.database import insert_to_table_meta_data
from models.api_models import ConvertCSVtoSQLTableResult
from src import *
from google import genai

def craft_tuned_prompt_for_each_file(table_name, df):
    table = connect_to_table(table_name)
    table_schema = get_table_schema(table)
    unique_elements = get_unique_elements(df)

    initial_prompt  = f"""
    Create a robust prompt appropriate for taking a question and creating a sql query to query the table.

    The following data will be useful to create the sql query:

    table_name:
    {table_name}

    table_schema:
    {table_schema}

    unique_elements:
    {unique_elements}

    End the prompt with:
    Now, please provide the natural language question for which you want a SQL query.
    """
    client = genai.Client(api_key=GOOGLE_API_KEY)
    # prompt = "Explain quantum computing in simple terms"
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=initial_prompt
    )
    try:
        return response.text
    except Exception as e:
        print(e)
        return ""

def connect_to_table(table_name):

  # Create engine
  engine = create_engine(CONN_STRING)

  # Create MetaData object
  metadata = MetaData()

  # Reflect the table from the database

  table = Table(table_name, metadata, autoload_with=engine)
  return table

def get_table_schema(table):
  table_schema = ""
  for column in table.columns:
      table_schema += f"Column: {column.name}, Type: {column.type}\n"
  return table_schema

def get_unique_elements(df):
  import numpy as np
  cols = df.columns
  df = df.replace(np.nan, None)
  unique_elements_prompt = ""
  for col in cols:
    unique_elements_prompt += f"Column: {col}, Unique elements: {df[col].unique()}\n"
  return unique_elements_prompt

def ingest_csv_to_database(csv_file_path):
    try:
        df = pd.read_csv(csv_file_path, index_col=0)
        engine = create_engine(CONN_STRING)
        table_name = csv_file_path.split("/")[-1].split(".")[0]
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        sql_prompt = craft_tuned_prompt_for_each_file(table_name, df)
        insert_to_table_meta_data(table_name, sql_prompt)

        if sql_prompt:
            return ConvertCSVtoSQLTableResult(table_name=table_name,status="Successfully ingested the csv file!")
        else:
            return ConvertCSVtoSQLTableResult(table_name=table_name,status="Failed to ingest the csv file!")
    except Exception as e:
        print(e)
        return ConvertCSVtoSQLTableResult(table_name=table_name,status="Failed to ingest the csv file!")