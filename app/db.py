from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, DATETIME, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from sqlalchemy.orm import Session

DATA_URL = "sqlite:///./app.db"

engine = create_engine(DATA_URL)

SessionLockal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLockal()
    try:
        yield db
    finally:
        db.close()

class Model(Base):
    name = Column(String, nullable=False, unique=True)

class User(Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    password = Column(Integer, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    is_admin = Column(Boolean, nullable=False, default=False)

class Tour(Model):
    __tablename__ = "tour"
    id = Column(Integer, primary_key=True)
    description = Column(Text, default=False)
    cost = Column(Integer, nullable=False)

