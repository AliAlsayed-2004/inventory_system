from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QMovie

class LoadingDialog(QDialog):
    def __init__(self, parent=None, message="جاري التصدير..."):
        super().__init__(parent)
        self.setWindowTitle(" ")
        self.setFixedSize(300, 120)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        self.label = QLabel(message)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 14px; color: white;")

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)  
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #00adb5;
                border-radius: 8px;
                text-align: center;
            }
        """)

        layout.addWidget(self.label)
        layout.addWidget(self.progress)

        QTimer.singleShot(15000, self.close)  