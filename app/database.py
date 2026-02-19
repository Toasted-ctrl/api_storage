import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

hostname = os.getenv("hostname")
database = os.getenv("database")
password = os.getenv("password")
username = os.getenv("user")
port = os.getenv("port")

engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{database}")
session_local = sessionmaker(autoflush=False, bind=engine)
base = declarative_base()

# TODO: Write tests for get_database()

def get_database():
    def database_session():
        database = session_local()
        try:
            yield database
        finally:
            database.close()
    return database_session

class Permissions(base):
    __tablename__ ='permissions'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    api_key = Column(String(100), nullable=False)
    is_admin = Column(Boolean, nullable=False)

base.metadata.create_all(engine)