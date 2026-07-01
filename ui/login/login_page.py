from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout
)

from ui.login.components.hero_panel import HeroPanel
from ui.login.components.login_card import LoginCard
from ui.login.login_animation import LoginAnimation
from PySide6.QtCore import QTimer
from ui.login.login_controller import LoginController

class LoginPage(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_ui()
        self.controller = LoginController(self.card)
        
    def setup_ui(self):

        layout = QHBoxLayout(self)

        layout.setContentsMargins(0,0,0,0)

        layout.setSpacing(0)

        self.hero = HeroPanel()

        self.card = LoginCard()
        self.anim = LoginAnimation(self.card)
        QTimer.singleShot(100, lambda: self.anim.slide_widget(self.card))

        self.hero.setMinimumWidth(600)

        self.card.setMinimumWidth(500)
        self.controller = LoginController(self.card)

        layout.addWidget(self.hero,3)

        layout.addWidget(self.card,2)