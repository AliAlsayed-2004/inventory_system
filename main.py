from PySide6.QtWidgets import QApplication
import sys
from ui.login import LoginWindow

app = QApplication(sys.argv)

window = LoginWindow()
window.show()

sys.exit(app.exec())