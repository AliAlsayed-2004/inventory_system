import pandas as pd
from datetime import datetime, timedelta
from database.db import SessionLocal
from models.item import Item
from models.transaction import Transaction
from sqlalchemy import func, and_


class ReportService:

    @staticmethod
    def export_items_to_excel(filename="inventory_items.xlsx"):
        db = SessionLocal()
        items = db.query(Item).all()
        db.close()

        data = [{
            "ID": item.id,
            "اسم الصنف": item.name,
            "التصنيف": item.category or "غير مصنف",
            "الكمية الحالية": item.quantity,
        } for item in items]

        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        return filename

    @staticmethod
    def export_transactions_to_excel(filename="transactions_report.xlsx"):
        db = SessionLocal()
        
        transactions = db.query(Transaction).all()

        data = []
        for t in transactions:
            item = db.query(Item).filter_by(id=t.item_id).first() if t.item_id else None
            item_name = item.name if item else f"Item #{t.item_id}"

            data.append({
                "ID": t.id,
                "اسم الصنف": item_name,
                "رقم الصنف": t.item_id,
                "نوع الحركة": t.action_type,
                "الكمية": t.quantity,
                "ملاحظات": t.note or "",
                "التاريخ": t.created_at.strftime("%Y-%m-%d %H:%M") if hasattr(t, 'created_at') else datetime.now().strftime("%Y-%m-%d %H:%M")
            })

        db.close()

        df = pd.DataFrame(data)
        df.to_excel(filename, index=False, sheet_name="Transactions")
        return filename

    @staticmethod
    def get_transactions_summary():
        db = SessionLocal()
        total = db.query(Transaction).count()
        db.close()
        return total