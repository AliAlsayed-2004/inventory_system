from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QFormLayout, QMessageBox)
from PySide6.QtCore import Qt

class EditItemDialog(QDialog):
    def __init__(self, item=None, parent=None):
        super().__init__(parent)
        self.item = item
        self.setWindowTitle("إضافة صنف" if not item else "تعديل صنف")
        self.setMinimumWidth(400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.name_input = QLineEdit(self.item.name if self.item else "")
        self.category_input = QLineEdit(self.item.category if self.item else "")
        self.quantity_input = QLineEdit(str(self.item.quantity) if self.item else "0")

        form.addRow("اسم الصنف:", self.name_input)
        form.addRow("التصنيف:", self.category_input)
        form.addRow("الكمية:", self.quantity_input)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("حفظ")
        cancel_btn = QPushButton("إلغاء")

        save_btn.clicked.connect(self.save)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

    def save(self):
        name = self.name_input.text().strip()
        category = self.category_input.text().strip()
        try:
            qty = int(self.quantity_input.text())
        except:
            QMessageBox.warning(self, "خطأ", "الكمية يجب أن تكون رقم")
            return

        if not name:
            QMessageBox.warning(self, "خطأ", "اسم الصنف مطلوب")
            return

        self.result = {"name": name, "category": category, "quantity": qty}
        self.accept()