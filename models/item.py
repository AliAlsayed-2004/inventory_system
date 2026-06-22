from sqlalchemy import Column, Integer, String
from database.db import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String)
    quantity = Column(Integer, default=0)