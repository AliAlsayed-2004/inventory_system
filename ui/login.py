from ui.dashboard import DashboardWindow
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtCore import QPropertyAnimation, QEasingCurve
import qtawesome as qta
from services.auth_service import login_user
from session import set_user


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login System")
        self.setFixedSize(400, 500)
        self.setStyleSheet(self.styles())

        self.init_ui()

        # animation
        self.setWindowOpacity(0)
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(800)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)

        self.anim.start()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Inventory System")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("title")

        # Username
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        icon = qta.icon("fa5s.user", color="white")
        self.username.addAction(icon, QLineEdit.LeadingPosition)

        # Password
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        icon = qta.icon("fa5s.lock", color="white")
        self.password.addAction(icon, QLineEdit.LeadingPosition)
        self.password.setEchoMode(QLineEdit.Password)

        # Button
        btn = QPushButton("Login")
        btn.clicked.connect(self.handle_login)

        # Message
        self.message = QLabel("")
        self.message.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(btn)
        layout.addWidget(self.message)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username.text()
        password = self.password.text()

        result = login_user(username, password)

        if isinstance(result, dict):
            set_user(result)

            self.dashboard = DashboardWindow()
            self.dashboard.show()

            self.close()
        else:
            self.message.setText(result)
            self.message.setStyleSheet("color: red;")

    def styles(self):
        return """
        QWidget {
            background-color: #121212;
            color: white;
            font-family: Arial;
            font-size: 14px;
        }

        #title {
            font-size: 24px;
            font-weight: bold;
            color: #00adb5;
        }

        QLineEdit {
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #333;
            background-color: #1e1e1e;
        }

        QLineEdit:focus {
            border: 1px solid #00adb5;
        }

        QPushButton {
            padding: 10px;
            border-radius: 8px;
            background-color: #00adb5;
            color: white;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #019ca3;
        }
        """