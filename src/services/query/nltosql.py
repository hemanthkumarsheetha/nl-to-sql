from src.db.models import TableMetaData
from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy.orm import sessionmaker
from src import *
from google import genai

def get_appropriate_prompt(table_name):
  engine = create_engine(CONN_STRING)
  # Create session factory
  Session = sessionmaker(bind=engine)

  # Insert using ORM
  session = Session()

  try:
    # Check if table_name already exists
    existing_record = session.query(TableMetaData).filter(
        TableMetaData.table_name == table_name
    ).first()
  except:
    return ""
  finally:
      session.close()
  
  if existing_record is None:
    return ""
  else:
    return existing_record.prompt

def get_sql_query_from_llm(prompt, natural_language_question):
  prompt += "\n" + natural_language_question
  client = genai.Client(api_key=GOOGLE_API_KEY)
  response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
  try:
    sql_query =  response.text
    post_process_prompt = f"""
    Clean and format the following SQL query. Return ONLY the clean SQL query with no additional text, formatting, or special characters.

    Requirements:
    - Remove all markdown formatting (```sql, ```)
    - Remove all backticks (`)
    - Remove all newlines and extra whitespace
    - Remove any explanatory text before or after the query
    - Return only the pure SQL query

    Example:
    Input: ```sql SELECT DISTINCT country FROM 'winemag-data-130k-v2';```
    Output: SELECT DISTINCT country FROM 'winemag-data-130k-v2';

    SQL Query to clean:
    {sql_query}
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=post_process_prompt
    )
    return response.text
  except Exception as e:
    print(e)
    return ""


def query_table_with_orm(table_name, sql_query):
    """
    Execute a SQL query on a specific table using SQLAlchemy ORM
    
    Args:
        table_name (str): Name of the table to query
        sql_query (str): SQL query string to execute
    
    Returns:
        list: Query results
    """
    from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    from datetime import datetime
    
    # Create engine
    engine = create_engine(CONN_STRING)
    
    # Create declarative base
    Base = declarative_base()
    
    # Create session factory
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Reflect the specific table from the database
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=engine)
        
        # Execute the SQL query on the specific table
        result = session.execute(text(sql_query))
        return result.fetchall()
    except Exception as e:
        print(f"Error executing query on table {table_name}: {e}")
        return []
    finally:
        session.close()


def craft_a_response(nl_query, table_filter):
  relevant_prompt = get_appropriate_prompt(table_filter)
  sql_query = get_sql_query_from_llm(relevant_prompt, nl_query)
  results = query_table_with_orm(table_filter, sql_query)

  client = genai.Client(api_key=GOOGLE_API_KEY)
  response_prompt = f"""
  Given an natural language query and its results, craft an appropriate response. You only return a response.

  Natural Language Query:
  {nl_query}

  Results:
  {results}

  Response:
  """
  response = client.models.generate_content(
      model="gemini-2.5-flash",
      contents=response_prompt
  )
  return response.text