from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, DATETIME, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from sqlalchemy.orm import Session


DATA_URL = "sqlite:///./db.db"


engine = create_engine(DATA_URL)


SessionLockal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()



def get_db():
    db = SessionLockal()
    try:
        yield db
    finally:
        db.close()


class NameFieldMixin(Base):
    __abstract__ = True
    name = Column(String, nullable=False, unique=True)


class User(NameFieldMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    password = Column(Integer, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    balance = Column(Integer, nullable=False, default=0)
    is_admin = Column(Boolean, nullable=False, default=False)


class Tour(NameFieldMixin):
    __tablename__ = "tour"
    id = Column(Integer, primary_key=True)
    description = Column(Text, default=False)
    price = Column(Integer, nullable=False)
    people = Column(Integer, nullable=False)
    from_time = Column(DATETIME, nullable=False)
    to_time = Column(DATETIME, nullable=False)
    picture = Column(Text, default="/static/images/default.png", nullable=False)


