from sqlalchemy import func
from database.db import SessionLocal
from models.item import Item


class InventoryStats:

    # -------------------------
    def get_total_items(self):
        db = SessionLocal()
        count = db.query(Item).count()
        db.close()
        return count

    # -------------------------
    def get_total_quantity(self):
        db = SessionLocal()
        total = db.query(func.sum(Item.quantity)).scalar()
        db.close()
        return total or 0

    # -------------------------
    def get_low_stock(self, threshold=5):
        db = SessionLocal()
        count = db.query(Item).filter(Item.quantity <= threshold).count()
        db.close()
        return count

    # -------------------------
    def get_categories_count(self):
        db = SessionLocal()
        count = db.query(Item.category).distinct().count()
        db.close()
        return count