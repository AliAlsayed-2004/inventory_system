from database.db import engine, Base

import models.user
import models.item
import models.transaction

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Database & Tables Created ✅")