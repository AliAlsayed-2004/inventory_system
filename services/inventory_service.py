from database.db import SessionLocal
from models.item import Item
from models.transaction import Transaction
from datetime import datetime


# --------------------- Item Functions ---------------------

def add_item(name, category, quantity):
    db = SessionLocal()

    item = Item(name=name, category=category, quantity=quantity)
    db.add(item)
    db.commit()

    transaction = Transaction(
        item_id=item.id,
        action_type="add",
        quantity=quantity,
        note="New item created",
        created_at=datetime.now()       # ← مهم
    )

    db.add(transaction)
    db.commit()
    db.close()
    return item

def get_item_by_id(item_id):
    db = SessionLocal()
    item = db.query(Item).get(item_id)

    if not item:
        return f"Item {item_id} Not Found"
    
    db.close()
    
    return item


def get_all_items():
    db = SessionLocal()
    items = db.query(Item).all()
    db.close()
    return items


def search_item(name):
    db = SessionLocal()
    items = db.query(Item).filter(Item.name.like(f"%{name}%")).all()
    db.close()
    return items


def update_item(item_id, new_name=None, new_category=None):
    db = SessionLocal()

    item = db.query(Item).get(item_id)

    if not item:
        return "Item not found"

    if new_name:
        item.name = new_name

    if new_category:
        item.category = new_category

    transaction = Transaction(
        item_id=item.id,
        item_name=item.name,
        action_type="update",
        quantity=0,
        note="تم تعديل البيانات",
        created_at=datetime.now()
    )

    db.add(transaction)
    db.commit()
    db.close()

    return item



def delete_item(item_id):
    db = SessionLocal()

    # حذف الحركات يدوياً (احتياطي)
    db.query(Transaction).filter_by(item_id=item_id).delete()

    item = db.query(Item).get(item_id)
    if item:
        db.delete(item)

    db.commit()
    db.close()

    return "Deleted"


# --------------------- Quantity Functions ---------------------

def increase_quantity(item_id, amount):
    db = SessionLocal()

    item = db.query(Item).get(item_id)

    if not item:
        return "Item not found"

    item.quantity += amount

    transaction = Transaction(
        item_id=item.id,
        action_type="add",
        quantity=amount,
        note="زيادة كمية",
        created_at=datetime.now()
    )

    db.add(transaction)
    db.commit()
    db.close()

    return item



def decrease_quantity(item_id, amount, note=None):
    db = SessionLocal()

    item = db.query(Item).get(item_id)
    if not item:
        db.close()
        return "Item not found"

    if item.quantity < amount:
        db.close()
        return "Not enough quantity"

    item.quantity -= amount

    transaction = Transaction(
        item_id=item.id,
        action_type="remove",
        quantity=amount,
        note=note or f"خصم كمية {amount} وحدة",
        created_at=datetime.now()
    )

    db.add(transaction)
    db.commit()
    db.close()

    return item




# --------------------- Transaction Functions ---------------------

def get_transactions(item_id):
    db = SessionLocal()

    if item_id:
        transactions = db.query(Transaction).filter_by(item_id=item_id).all()
    else:
        return f"Item {item_id} Not Found"

    db.close()
    return transactions


def get_all_transactions():
    db = SessionLocal()
    transactions = db.query(Transaction).all()
    db.close()
    return transactions


