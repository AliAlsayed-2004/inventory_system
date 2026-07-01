from PySide6.QtWidgets import QWidget, QHBoxLayout, QFrame, QVBoxLayout, QStackedWidget, QPushButton, QMessageBox
from PySide6.QtCore import Qt

from ui.dashboard.pages.overview import OverviewPage
from ui.dashboard.pages.items import ItemsPage
from ui.dashboard.pages.reports import ReportsPage   


class DashboardWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.resize(1300, 780)
        self.setWindowTitle("Inventory Dashboard")
        self.current_page = None

        self.init_ui()

    def init_ui(self):

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ================= SIDEBAR =================
        self.sidebar = self.create_sidebar()

        # ================= CONTENT =================
        self.content_container = QFrame()
        self.stack = QStackedWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.addWidget(self.stack)

        # Create pages
        self.overview = OverviewPage()
        self.items = ItemsPage()
        self.reports = ReportsPage()          

        self.stack.addWidget(self.overview)
        self.stack.addWidget(self.items)
        self.stack.addWidget(self.reports)

        root.addWidget(self.sidebar)
        root.addWidget(self.content_container, 1)

    # ---------------- SIDEBAR ----------------
    def create_sidebar(self):

        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            background-color: #111827;
            color: white;
        """)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 30, 20, 20)
        layout.setSpacing(12)

        # Header
        title = QPushButton("📦 Inventory Pro")
        title.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                font-weight: bold;
                padding: 15px;
                text-align: left;
                border: none;
            }
        """)
        layout.addWidget(title)

        # Navigation Buttons
        btn_overview = QPushButton("📊 نظرة عامة")
        btn_items = QPushButton("📦 ادارة العناصر")
        btn_reports = QPushButton("📈 التقارير")
        btn_profile = QPushButton("👤 الملف الشخصي")
        btn_backup = QPushButton("💾 انشاء نسخة احتياطية")

        for btn in [btn_overview, btn_items, btn_reports, btn_profile, btn_backup]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1F2937;
                    color: white;
                    padding: 14px 18px;
                    border-radius: 10px;
                    text-align: left;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #374151;
                }
                QPushButton:pressed {
                    background-color: #00adb5;
                }
            """)

        # Connect buttons
        btn_overview.clicked.connect(lambda: self.stack.setCurrentWidget(self.overview))
        btn_items.clicked.connect(lambda: self.stack.setCurrentWidget(self.items))
        btn_reports.clicked.connect(lambda: self.stack.setCurrentWidget(self.reports))
        btn_profile.clicked.connect(self.show_profile)
        btn_backup.clicked.connect(self.create_backup)

        layout.addWidget(btn_overview)
        layout.addWidget(btn_items)
        layout.addWidget(btn_reports)
        layout.addWidget(btn_profile)
        layout.addWidget(btn_backup)
        layout.addStretch()

        # Logout
        logout_btn = QPushButton("🚪 تسجيل الخروج")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                padding: 12px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)

        return sidebar

    def show_profile(self):
        from ui.dashboard.dialogs.user_profile import UserProfileDialog
        dialog = UserProfileDialog(self)
        dialog.exec()

    def logout(self):
        reply = QMessageBox.question(self, "تسجيل الخروج", 
                                   "هل أنت متأكد من تسجيل الخروج؟",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            from utils.session import set_user
            set_user(None)
            self.close()
            
            from ui.login.login_window import LoginWindow
            login = LoginWindow()
            login.show()
    
    def create_backup(self):
        from utils.backup import create_backup
        create_backup(self)