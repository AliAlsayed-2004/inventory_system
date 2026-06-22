from sqlalchemy import Column, Integer, String
from database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # hashed password
    full_name = Column(String)