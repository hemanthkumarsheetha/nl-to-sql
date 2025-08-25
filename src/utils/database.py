import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.db.models import TableMetaData
from src import CONN_STRING

def insert_to_table_meta_data(table_name, prompt):
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

    # Only insert if table_name doesn't exist
    if existing_record is None:
      # Single insert
      new_user = TableMetaData(
        table_name = table_name,
        prompt = prompt,
        created_at = datetime.datetime.now(datetime.timezone.utc)
      )
      session.add(new_user)
      session.commit()

  except Exception as e:
      session.rollback()
      raise e
  finally:
      session.close()