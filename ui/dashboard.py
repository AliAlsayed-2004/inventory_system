import sys
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem
)
from PySide6.QtCore import Qt,  QPropertyAnimation, QEasingCurve

from services.inventory_service import get_all_items


class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dashboard")
        self.setMinimumSize(900, 600)
        self.setStyleSheet(self.styles())

        self.init_ui()
        self.setWindowOpacity(0)
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(800)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)

        self.anim.start()
        self.load_data()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # ===== Header =====
        title = QLabel("📊 Inventory Dashboard")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("title")

        # ===== Stats Cards =====
        stats_layout = QHBoxLayout()

        self.total_items = QLabel("Items: 0")
        self.total_qty = QLabel("Quantity: 0")

        stats_layout.addWidget(self.total_items)
        stats_layout.addWidget(self.total_qty)

        # ===== Table =====
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Category", "Quantity"])

        # ===== Buttons =====
        btn_layout = QHBoxLayout()

        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_data)

        btn_layout.addWidget(refresh_btn)

        # ===== Add to layout =====
        main_layout.addWidget(title)
        main_layout.addLayout(stats_layout)
        main_layout.addWidget(self.table)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    def load_data(self):
        items = get_all_items()

        self.table.setRowCount(len(items))

        total_qty = 0

        for row, item in enumerate(items):
            self.table.setItem(row, 0, QTableWidgetItem(item.name))
            self.table.setItem(row, 1, QTableWidgetItem(item.category))
            self.table.setItem(row, 2, QTableWidgetItem(str(item.quantity)))

            total_qty += item.quantity

        self.total_items.setText(f"📦 Items: {len(items)}")
        self.total_qty.setText(f"📊 Quantity: {total_qty}")

    def styles(self):
        return """
        QWidget {
            background-color: #121212;
            color: white;
            font-size: 14px;
        }

        #title {
            font-size: 24px;
            font-weight: bold;
            color: #00adb5;
        }

        QLabel {
            padding: 10px;
            background-color: #1e1e1e;
            border-radius: 10px;
        }

        QTableWidget {
            background-color: #1e1e1e;
            border-radius: 10px;
            gridline-color: #333;
        }

        QHeaderView::section {
            background-color: #00adb5;
            padding: 6px;
            border: none;
        }

        QPushButton {
            padding: 10px;
            border-radius: 8px;
            background-color: #00adb5;
        }

        QPushButton:hover {
            background-color: #019ca3;
        }
        """