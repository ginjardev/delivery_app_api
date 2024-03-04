from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/pizza_delivery"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
Base = declarative_base()
SessionLocal = sessionmaker()
