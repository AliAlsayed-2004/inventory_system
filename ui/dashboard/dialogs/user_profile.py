from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QMessageBox, QFormLayout)
from PySide6.QtCore import Qt
from services.auth_service import check_password, hash_password
from database.db import SessionLocal
from models.user import User
from utils.session import get_user


class UserProfileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_user = get_user()
        
        if not self.current_user:
            QMessageBox.warning(self, "خطأ", "لم يتم العثور على بيانات المستخدم")
            self.reject()
            return

        self.setWindowTitle("تعديل بيانات المستخدم")
        self.setMinimumWidth(480)
        self.user_obj = None
        self.init_ui()

    def init_ui(self):
        with SessionLocal() as db:
            self.user_obj = db.query(User).filter_by(id=self.current_user["user_id"]).first()

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.full_name = QLineEdit(self.user_obj.full_name if self.user_obj else "")
        self.username = QLineEdit(self.user_obj.username if self.user_obj else "")
        
        self.current_password = QLineEdit()
        self.current_password.setEchoMode(QLineEdit.Password)
        
        self.new_password = QLineEdit()
        self.new_password.setEchoMode(QLineEdit.Password)
        
        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.Password)

        form.addRow("الاسم الكامل:", self.full_name)
        form.addRow("اسم المستخدم:", self.username)
        form.addRow("كلمة المرور الحالية *:", self.current_password)
        form.addRow("كلمة مرور جديدة (اختياري):", self.new_password)
        form.addRow("تأكيد كلمة المرور:", self.confirm_password)

        layout.addLayout(form)

        # Note
        note = QLabel("اترك حقل كلمة المرور فارغاً إذا لا تريد تغييرها")
        note.setStyleSheet("color: #9ca3af; font-size: 12px;")
        layout.addWidget(note)

        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("حفظ التغييرات")
        cancel_btn = QPushButton("إلغاء")

        save_btn.clicked.connect(self.save_changes)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

    def save_changes(self):
        if not self.current_password.text().strip():
            QMessageBox.warning(self, "خطأ", "يجب إدخال كلمة المرور الحالية")
            return

        with SessionLocal() as db:
            user = db.query(User).filter_by(id=self.current_user["user_id"]).first()
            
            if not user or not check_password(self.current_password.text().strip(), user.password):
                QMessageBox.warning(self, "خطأ", "كلمة المرور الحالية غير صحيحة")
                return

            # Update info
            if self.full_name.text().strip():
                user.full_name = self.full_name.text().strip()
            if self.username.text().strip():
                user.username = self.username.text().strip()

            new_pass = self.new_password.text().strip()
            if new_pass:
                if new_pass != self.confirm_password.text().strip():
                    QMessageBox.warning(self, "خطأ", "كلمات المرور غير متطابقة")
                    return
                user.password = hash_password(new_pass).decode('utf-8')

            db.commit()

        QMessageBox.information(self, "نجاح", "تم تحديث البيانات بنجاح")
        self.accept()