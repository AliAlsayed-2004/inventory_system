from PySide6.QtCore import QObject, QTimer
from qfluentwidgets import InfoBar, InfoBarPosition
from services.auth_service import login_user
from utils.session import set_user


class LoginController(QObject):

    def __init__(self, view):
        super().__init__()
        self.view = view
        self.connect_signals()

    def connect_signals(self):
        self.view.login_btn.clicked.connect(self.handle_login)

    # -------------------------
    # LOGIN LOGIC
    # -------------------------
    def handle_login(self):

        username = self.view.username.text().strip()
        password = self.view.password.text().strip()

        if not username or not password:
            self.show_error("يرجى تعبئة جميع الحقول")
            return

        # Loading state
        self.view.login_btn.setText("جاري تسجيل الدخول...")
        self.view.login_btn.setEnabled(False)

        # Real login with small delay for better UX
        QTimer.singleShot(800, lambda: self.real_login(username, password))

    def real_login(self, username, password):
        result = login_user(username, password)

        if isinstance(result, dict):
            set_user(result)
            self.show_success("تم تسجيل الدخول بنجاح")
            QTimer.singleShot(600, self.open_dashboard)
        else:
            self.show_error(result)
            self.reset_button()

    # -------------------------
    # DASHBOARD
    # -------------------------
    def open_dashboard(self):
        from ui.dashboard.dashboard import DashboardWindow

        self.dashboard = DashboardWindow()
        self.dashboard.show()
        self.view.window().close()

    # -------------------------
    # UI Helpers
    # -------------------------
    def reset_button(self):
        self.view.login_btn.setText("Login")
        self.view.login_btn.setEnabled(True)

    def show_error(self, msg):
        InfoBar.error(
            title="خطأ",
            content=msg,
            parent=self.view,
            position=InfoBarPosition.TOP,
            duration=3000
        )

    def show_success(self, msg):
        InfoBar.success(
            title="نجاح",
            content=msg,
            parent=self.view,
            position=InfoBarPosition.TOP,
            duration=1500
        )