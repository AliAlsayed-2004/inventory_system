from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from database.db import Base
from datetime import datetime

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id", ondelete="CASCADE"))
    action_type = Column(String)
    quantity = Column(Integer)
    note = Column(String)
    
    # حل المشكلة
    created_at = Column(DateTime(timezone=True), 
                       server_default=func.now(), 
                       default=func.now())   # ← أضف default