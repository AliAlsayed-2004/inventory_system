from PySide6.QtWidgets import QWidget, QHBoxLayout
from ui.login.login_page import LoginPage
from ui.login.login_animation import LoginAnimation


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.resize(1200, 700)
        self.setWindowTitle("Inventory System")

        self.init_ui()

        # 👇 Animation system
        self.anim = LoginAnimation(self)
        self.anim.fade_in()

    def init_ui(self):

        layout = QHBoxLayout(self)

        self.page = LoginPage()

        layout.addWidget(self.page)