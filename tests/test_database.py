from database.db import SessionLocal
from models.item import Item

db = SessionLocal()

new_item = Item(name="Laptop", category="Electronics", quantity=10)

db.add(new_item)
db.commit()

print("Item Added ✅")