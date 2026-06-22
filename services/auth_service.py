import bcrypt
from database.db import SessionLocal
from models.user import User

def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def check_password(password: str, hashed: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)


def register_user(username, password, full_name):
    db = SessionLocal()

    # check if user exists
    existing = db.query(User).filter_by(username=username).first()
    if existing:
        return "User already exists"

    hashed = hash_password(password)

    user = User(
        username=username,
        password=hashed.decode('utf-8'),
        full_name=full_name
    )

    db.add(user)
    db.commit()
    db.close()

    return "User created successfully"



def login_user(username, password):
    db = SessionLocal()

    user = db.query(User).filter_by(username=username).first()

    if not user:
        return "User not found"

    if check_password(password, user.password.encode('utf-8')):
        return {
            "status": "success",
            "user_id": user.id,
            "username": user.username
        }

    return "Wrong password"