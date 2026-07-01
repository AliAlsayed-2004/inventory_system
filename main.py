from PySide6.QtWidgets import QApplication
import sys
from ui.login.login_window import LoginWindow
from utils.theme import load_stylesheet

app = QApplication(sys.argv)
load_stylesheet(app, "assets/qss/login.qss")

window = LoginWindow()
window.show()

sys.exit(app.exec())