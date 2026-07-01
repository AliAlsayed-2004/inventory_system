from services.auth_service import *

print(register_user("admin", "123456", "Administrator"))

print(login_user("admin", "123456"))