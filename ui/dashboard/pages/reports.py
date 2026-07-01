from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QComboBox, QLineEdit
)
from PySide6.QtCore import Qt, QTimer
from services.report_service import ReportService
from services.inventory_service import get_all_transactions, get_item_by_id
from datetime import datetime


class ReportsPage(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_data()

    def init_ui(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(25, 25, 25, 25)
        main.setSpacing(20)

        title = QLabel("📈 Reports & Analytics")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: white;")
        main.addWidget(title)

        # Advanced Filter
        filter_layout = QHBoxLayout()

        # Search by name
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 ابحث باسم الصنف...")
        self.search_input.textChanged.connect(self.load_data)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["الكل", "آخر 7 أيام", "آخر 30 يوم", "آخر 90 يوم"])
        self.filter_combo.currentTextChanged.connect(self.load_data)

        self.refresh_btn = QPushButton("🔄 تحديث")

        # Export buttons...
        self.btn_export_items = QPushButton("📊 تصدير الأصناف")
        self.btn_export_trans = QPushButton("📋 تصدير الحركات")

        self.refresh_btn.clicked.connect(self.refresh_with_animation)
        self.btn_export_items.clicked.connect(self.export_items)
        self.btn_export_trans.clicked.connect(self.export_transactions)

        filter_layout.addWidget(self.search_input, 2)
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addStretch()
        filter_layout.addWidget(self.refresh_btn)
        filter_layout.addWidget(self.btn_export_items)
        filter_layout.addWidget(self.btn_export_trans)

        main.addLayout(filter_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "التاريخ", "الصنف", "نوع الحركة", "الكمية", "ملاحظات"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        main.addWidget(self.table)

    def load_data(self):
        transactions = get_all_transactions()
        search_text = self.search_input.text().strip().lower()

        # Filter by search
        if search_text:
            filtered = []
            for t in transactions:
                item = get_item_by_id(t.item_id)
                item_name = item.name.lower() if hasattr(item, 'name') else ""
                if search_text in item_name:
                    filtered.append(t)
            transactions = filtered

        # Sort by date desc
        transactions = sorted(transactions, 
                            key=lambda t: t.created_at if hasattr(t, 'created_at') and t.created_at else datetime.min,
                            reverse=True)

        self.table.setRowCount(len(transactions))

        for row, t in enumerate(transactions):
            item = get_item_by_id(t.item_id)
            item_name = item.name if hasattr(item, 'name') else f"Item #{t.item_id}"

            trans_date = t.created_at.strftime("%Y-%m-%d %I:%M %p") if hasattr(t, 'created_at') and t.created_at else "غير متوفر"

            self.table.setItem(row, 0, QTableWidgetItem(str(t.id)))
            self.table.setItem(row, 1, QTableWidgetItem(trans_date))
            self.table.setItem(row, 2, QTableWidgetItem(item_name))
            self.table.setItem(row, 3, QTableWidgetItem(t.action_type))
            self.table.setItem(row, 4, QTableWidgetItem(str(t.quantity)))
            self.table.setItem(row, 5, QTableWidgetItem(t.note or "-"))

    def export_items(self):
        try:
            filename = ReportService.export_items_to_excel()
            QMessageBox.information(self, "نجاح", f"تم التصدير:\n{filename}")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", str(e))

    def export_transactions(self):
        try:
            filename = ReportService.export_transactions_to_excel()
            QMessageBox.information(self, "نجاح", f"تم التصدير:\n{filename}")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", str(e))

    def refresh_with_animation(self):
        """تحديث مع أيقونة تتحرك"""
        self.refresh_btn.setText("⏳ جاري التحديث...")
        self.refresh_btn.setEnabled(False)

        self.load_data()

        QTimer.singleShot(800, self.finish_refresh)

    def finish_refresh(self):
        self.refresh_btn.setText("🔄 تحديث")
        self.refresh_btn.setEnabled(True)
        
        # Flash effect
        original_style = self.refresh_btn.styleSheet()
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 18px;
                border-radius: 8px;
                font-weight: bold;
                background-color: #10b981;
                color: white;
            }
        """)
        QTimer.singleShot(1200, lambda: self.refresh_btn.setStyleSheet(original_style))