import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from database.db import SessionLocal
from models.item import Item
from sqlalchemy import func


class ChartService:

    @staticmethod
    def get_top_items_by_quantity(limit=5):
        db = SessionLocal()
        items = db.query(Item).order_by(Item.quantity.desc()).limit(limit).all()
        db.close()
        return items

    @staticmethod
    def get_category_distribution():
        db = SessionLocal()
        result = db.query(
            Item.category, 
            func.sum(Item.quantity).label('total')
        ).group_by(Item.category).all()
        db.close()
        return result