from PySide6.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import (
    LineEdit,
    PasswordLineEdit,
    CheckBox,
    PrimaryPushButton,
    BodyLabel,
    TitleLabel
)
from PySide6.QtCore import Qt


class LoginCard(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.setObjectName("LoginCard")
        self.setStyleSheet("color: #F9FAFB;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 60, 50, 60)
        layout.setSpacing(18)

        # ================= TITLE =================
        title = TitleLabel("Welcome Back")
        title.setStyleSheet("color: #F9FAFB;")
        subtitle = BodyLabel("Sign in to continue to Inventory System")
        subtitle.setStyleSheet("color: #9CA3AF;")

        # ================= INPUTS =================
        self.username = LineEdit()
        self.username.setPlaceholderText("اسم المستخدم")
        layout.addWidget(self.username)

        self.password = PasswordLineEdit()
        self.password.setPlaceholderText("كلمة السر")
        layout.addWidget(self.password)

        # ================= CHECKBOX =================
        self.remember = CheckBox("Remember me")
        self.remember.setStyleSheet("color: #F9FAFB;")
        layout.addWidget(self.remember)

        # ================= BUTTON =================
        self.login_btn = PrimaryPushButton("تسجيل الدخول")
        layout.addWidget(self.login_btn)

        # ================= ADD WIDGETS =================
        layout.addWidget(title, alignment=Qt.AlignCenter)
        layout.addWidget(subtitle, alignment=Qt.AlignCenter)

        layout.addSpacing(20)

        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.remember)
        layout.addSpacing(10)
        layout.addWidget(self.login_btn)

        # Enable Enter key to login
        self.password.returnPressed.connect(self.login_btn.click)
        self.username.returnPressed.connect(self.password.setFocus)