from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)

from PySide6.QtGui import (
    QPixmap,
    QFont
)

from PySide6.QtCore import Qt
from utils.helper import asset


class HeroPanel(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(40,40,40,40)
        layout.setSpacing(20)

        layout.setAlignment(Qt.AlignCenter)

        # -----------------------------
        # Logo
        # -----------------------------

        self.logo = QLabel()

        pixmap = QPixmap(asset("images/logo.png"))

        self.logo.setPixmap(
            pixmap.scaled(
                120,
                120,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

        self.logo.setAlignment(Qt.AlignCenter)

        # -----------------------------
        # Title
        # -----------------------------

        self.title = QLabel("Inventory Pro")

        font = QFont("Inter",24)
        font.setBold(True)

        self.title.setFont(font)

        self.title.setAlignment(Qt.AlignCenter)

        # -----------------------------
        # Subtitle
        # -----------------------------

        self.subtitle = QLabel(
            "Smart Inventory Management System"
        )

        font2 = QFont("Inter",12)

        self.subtitle.setFont(font2)

        self.subtitle.setAlignment(Qt.AlignCenter)

        self.subtitle.setWordWrap(True)

        # -----------------------------
        # Illustration
        # -----------------------------

        self.image = QLabel()

        illustration = QPixmap(
            asset("images/login_illustration.png")
        )

        self.image.setPixmap(

            illustration.scaled(

                420,

                420,

                Qt.KeepAspectRatio,

                Qt.SmoothTransformation

            )

        )

        self.image.setAlignment(Qt.AlignCenter)

        layout.addStretch()

        layout.addWidget(self.logo)

        layout.addWidget(self.title)

        layout.addWidget(self.subtitle)

        layout.addSpacing(20)

        layout.addWidget(self.image)

        layout.addStretch()