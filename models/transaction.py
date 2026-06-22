from sqlalchemy import Column, Integer, String, ForeignKey
from database.db import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    action_type = Column(String)  # add / remove / update
    quantity = Column(Integer)
    note = Column(String)