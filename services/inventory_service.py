from database.db import SessionLocal
from models.item import Item
from models.transaction import Transaction

def add_item(name, category, quantity):
    db = SessionLocal()

    item = Item(name=name, category=category, quantity=quantity)
    db.add(item)
    db.commit()

    # تسجيل الحركة
    transaction = Transaction(
        item_id=item.id,
        action_type="add",
        quantity=quantity,
        note="New item created"
    )

    db.add(transaction)
    db.commit()

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
        note="زيادة كمية"
    )

    db.add(transaction)
    db.commit()
    db.close()

    return item




def decrease_quantity(item_id, amount):
    db = SessionLocal()

    item = db.query(Item).get(item_id)

    if not item:
        return "Item not found"

    if item.quantity < amount:
        return "Not enough quantity"

    item.quantity -= amount

    transaction = Transaction(
        item_id=item.id,
        action_type="remove",
        quantity=amount,
        note="خصم كمية"
    )

    db.add(transaction)
    db.commit()
    db.close()

    return item


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
        action_type="update",
        quantity=0,
        note="تم تعديل البيانات"
    )

    db.add(transaction)
    db.commit()
    db.close()

    return item



def delete_item(item_id):
    db = SessionLocal()

    item = db.query(Item).get(item_id)

    if not item:
        return "Item not found"

    db.delete(item)
    db.commit()
    db.close()

    return "Deleted"


def get_transactions(item_id=None):
    db = SessionLocal()

    if item_id:
        transactions = db.query(Transaction).filter_by(item_id=item_id).all()
    else:
        transactions = db.query(Transaction).all()

    db.close()
    return transactions