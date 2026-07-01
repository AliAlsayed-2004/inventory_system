from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QRect


class LoginAnimation:

    def __init__(self, window):
        self.window = window

    def fade_in(self):
        self.window.setWindowOpacity(0)

        self.anim = QPropertyAnimation(self.window, b"windowOpacity")
        self.anim.setDuration(600)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.start()

    def slide_widget(self, widget):

        # نخزن المكان الحقيقي النهائي بعد layout
        final_geom = widget.geometry()

        # نبدأ من اليمين (خارج الشاشة شوي)
        start_geom = QRect(
            final_geom.x() + 80,
            final_geom.y(),
            final_geom.width(),
            final_geom.height()
        )

        widget.setGeometry(start_geom)

        self.anim2 = QPropertyAnimation(widget, b"geometry")
        self.anim2.setDuration(700)
        self.anim2.setStartValue(start_geom)
        self.anim2.setEndValue(final_geom)
        self.anim2.setEasingCurve(QEasingCurve.OutCubic)
        self.anim2.start()