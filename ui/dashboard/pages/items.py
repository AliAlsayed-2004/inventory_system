from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QLineEdit, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton, QMessageBox, QDialog
)
from PySide6.QtCore import Qt, QTimer

from services.inventory_service import get_all_items, search_item, add_item, update_item, delete_item
from ui.dashboard.dialogs.edit_item import EditItemDialog
from ui.dashboard.dialogs.quantity_dialog import QuantityDialog

class ItemsPage(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_data()

    # ================= UI =================
    def init_ui(self):

        self.setStyleSheet("background-color: transparent;")

        main = QVBoxLayout(self)
        main.setContentsMargins(25, 25, 25, 25)
        main.setSpacing(18)

        # ================= TITLE =================
        title = QLabel("📦 Items Management")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: white;
        """)
        main.addWidget(title)

        # ================= KPI ROW =================
        kpi_row = QHBoxLayout()
        kpi_row.setSpacing(15)

        self.kpi_total = self.create_card("Total Items", "0")
        self.kpi_stock = self.create_card("Total Stock", "0")
        self.kpi_low = self.create_card("Low Stock", "0")

        kpi_row.addWidget(self.kpi_total)
        kpi_row.addWidget(self.kpi_stock)
        kpi_row.addWidget(self.kpi_low)

        main.addLayout(kpi_row)

        # ================= SEARCH =================
        self.search = QLineEdit()
        self.search.setPlaceholderText("🔍 Search items by name...")

        self.search.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border-radius: 10px;
                background-color: #1F2937;
                color: white;
                border: 1px solid #374151;
                font-size: 13px;
            }
        """)

        self.search.textChanged.connect(self.on_search)
        main.addWidget(self.search)

        # ================= TABLE =================
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Name", "Category", "Quantity"]
        )

        # مهم جداً لحل مشكلة الشكل 👇
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #111827;
                color: white;
                border-radius: 12px;
                gridline-color: #1F2937;
                font-size: 13px;
            }

            QHeaderView::section {
                background-color: #1F2937;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }

            QTableWidget::item {
                padding: 10px;
            }

            QTableWidget::item:selected {
                background-color: #2563EB;
            }
        """)

        main.addWidget(self.table)

    # ================= BUTTONS =================
        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("➕ إضافة صنف جديد")
        self.increase_btn = QPushButton("📈 إضافة كمية")
        self.decrease_btn = QPushButton("📉 خصم كمية")
        self.edit_btn = QPushButton("✏️ تعديل")
        self.delete_btn = QPushButton("🗑️ حذف")
        self.export_btn = QPushButton("📊 تصدير إلى Excel")
        self.refresh_btn = QPushButton("🔄 تحديث")


        self.add_btn.clicked.connect(self.add_item)
        self.increase_btn.clicked.connect(self.increase_quantity)
        self.decrease_btn.clicked.connect(self.decrease_quantity_ui)
        self.edit_btn.clicked.connect(self.edit_item)
        self.delete_btn.clicked.connect(self.delete_item)
        self.export_btn.clicked.connect(self.export_to_excel)
        self.refresh_btn.clicked.connect(self.refresh_with_animation)

        for btn in [self.add_btn, self.increase_btn, self.decrease_btn, 
                        self.edit_btn, self.delete_btn, self.refresh_btn]:
                    btn.setStyleSheet("""
                        QPushButton {
                            padding: 10px 16px;
                            border-radius: 8px;
                            font-weight: bold;
                        }
                    """)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.increase_btn)
        btn_layout.addWidget(self.decrease_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.export_btn)
        btn_layout.addWidget(self.refresh_btn)

        btn_layout.addStretch()

        main.addLayout(btn_layout)
        main.addWidget(self.table)

    # ================= CARD =================
    def create_card(self, title, value):

        card = QFrame()
        card.setFixedHeight(90)
        card.setStyleSheet("""
            background-color: #1F2937;
            border-radius: 12px;
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 10, 15, 10)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #9CA3AF; font-size: 12px;")

        lbl_value = QLabel(value)
        lbl_value.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_value)

        return card

    # ================= LOAD DATA =================
    def load_data(self, data=None):

        if data is None:
            data = get_all_items()

        self.table.setRowCount(len(data))

        total_stock = 0

        for row, item in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(str(item.id)))
            self.table.setItem(row, 1, QTableWidgetItem(item.name))
            self.table.setItem(row, 2, QTableWidgetItem(item.category))
            self.table.setItem(row, 3, QTableWidgetItem(str(item.quantity)))

            total_stock += item.quantity

        # تحديث الكروت
        self.kpi_total.findChildren(QLabel)[1].setText(str(len(data)))
        self.kpi_stock.findChildren(QLabel)[1].setText(str(total_stock))

    # ================= SEARCH =================
    def on_search(self, text):

        if text.strip() == "":
            self.load_data()
        else:
            self.load_data(search_item(text))

    # ================= ADD ITEM =================
    def add_item(self):
        dialog = EditItemDialog()
        if dialog.exec() == QDialog.Accepted:
            data = dialog.result
            add_item(data['name'], data['category'], data['quantity'])
            self.load_data()
            QMessageBox.information(self, "نجح", "تم إضافة الصنف بنجاح")

    def edit_item(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "تنبيه", "اختر صنف أولاً")
            return

        item_id = int(self.table.item(row, 0).text())
        # يجب تعديل service لجلب item
        from services.inventory_service import get_item_by_id
        item = get_item_by_id(item_id)

        dialog = EditItemDialog(item)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.result
            update_item(item_id, data['name'], data['category'])
            # يمكن تحديث الكمية أيضاً لاحقاً
            self.load_data()
            QMessageBox.information(self, "نجح", "تم التعديل بنجاح")

    def delete_item(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "تنبيه", "اختر صنف أولاً")
            return

        item_id = int(self.table.item(row, 0).text())
        name = self.table.item(row, 1).text()

        reply = QMessageBox.question(self, "تأكيد الحذف", 
                                   f"هل أنت متأكد من حذف {name}؟",
                                   QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            from services.inventory_service import delete_item
            delete_item(item_id)
            self.load_data()
            QMessageBox.information(self, "نجح", "تم الحذف بنجاح")


    def export_to_excel(self):
        from services.report_service import ReportService
        from ui.dashboard.dialogs.loading_dialog import LoadingDialog
        
        loading = LoadingDialog(self, "جاري تصدير البيانات إلى Excel...")
        loading.show()
        # استخدام QTimer عشان ما يعلق الـ UI
        QTimer.singleShot(100, lambda: self._do_export(loading))

    def _do_export(self, loading_dialog):
        from services.report_service import ReportService
        from PySide6.QtWidgets import QMessageBox
        
        try:
            filename = ReportService.export_items_to_excel()
            loading_dialog.close()
            QMessageBox.information(self, "نجح التصدير", 
                                f"تم تصدير البيانات بنجاح إلى:\n{filename}\n\nالملف محفوظ في مجلد المشروع.")
        except Exception as e:
            loading_dialog.close()
            QMessageBox.critical(self, "خطأ في التصدير", f"حدث خطأ: {str(e)}")


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
        original = self.refresh_btn.styleSheet()
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 16px;
                border-radius: 8px;
                font-weight: bold;
                background-color: #10b981;
                color: white;
            }
        """)
        QTimer.singleShot(1200, lambda: self.refresh_btn.setStyleSheet(original))

    def increase_quantity(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "تنبيه", "اختر صنف أولاً")
            return

        item_id = int(self.table.item(row, 0).text())
        item_name = self.table.item(row, 1).text()

        dialog = QuantityDialog(item_name, action_type="add")
        if dialog.exec() == QDialog.Accepted:
            amount, note = dialog.get_data()
            if amount > 0:
                from services.inventory_service import increase_quantity
                result = increase_quantity(item_id, amount)
                self.load_data()
                QMessageBox.information(self, "نجاح", f"تمت إضافة {amount} وحدة")

    def decrease_quantity_ui(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "تنبيه", "اختر صنف أولاً")
            return

        item_id = int(self.table.item(row, 0).text())
        item_name = self.table.item(row, 1).text()

        dialog = QuantityDialog(item_name, action_type="remove")
        if dialog.exec() == QDialog.Accepted:
            amount, note = dialog.get_data()
            if amount > 0:
                from services.inventory_service import decrease_quantity
                result = decrease_quantity(item_id, amount, note)
                if isinstance(result, str) and "enough" in result:
                    QMessageBox.warning(self, "خطأ", "الكمية غير كافية")
                else:
                    self.load_data()
                    QMessageBox.information(self, "نجاح", f"تم خصم {amount} وحدة")    