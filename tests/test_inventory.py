from services.inventory_service import *

# إضافة
add_item("Mouse", "Electronics", 20)

# عرض
items = get_all_items()
for item in items:
    print(item.name, item.quantity)

# زيادة
increase_quantity(1, 5)

# خصم
decrease_quantity(1, 2)