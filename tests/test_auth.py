from services.auth_service import *

# تسجيل مستخدم
print(register_user("admin", "123456", "Administrator"))

# تسجيل دخول
print(login_user("admin", "123456"))