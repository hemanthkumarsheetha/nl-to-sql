from src import CONN_STRING
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Create engine
engine = create_engine(CONN_STRING)

# Create declarative base
Base = declarative_base()

# Define table as a class
class TableMetaData(Base):
    __tablename__ = 'table-meta-data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String(255), nullable=False)
    prompt = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

# Create all tables
# Base.metadata.create_all(engine)

# Create session factory
# Session = sessionmaker(bind=engine)