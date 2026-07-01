from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QMessageBox, QFormLayout)
from PySide6.QtCore import Qt

class QuantityDialog(QDialog):
    def __init__(self, item_name, action_type="add", parent=None):  # action_type: "add" or "remove"
        super().__init__(parent)
        self.action_type = action_type
        self.setWindowTitle("إضافة كمية" if action_type == "add" else "خصم كمية")
        self.setMinimumWidth(400)
        self.init_ui(item_name)

    def init_ui(self, item_name):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.amount_input = QLineEdit("10")
        self.note_input = QLineEdit("")

        form.addRow("الصنف:", QLabel(item_name))
        form.addRow("الكمية:", self.amount_input)
        form.addRow("ملاحظات:", self.note_input)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        confirm_btn = QPushButton("تأكيد" if self.action_type == "add" else "خصم")
        cancel_btn = QPushButton("إلغاء")

        confirm_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(confirm_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

    def get_data(self):
        try:
            amount = int(self.amount_input.text())
        except:
            amount = 0
        note = self.note_input.text().strip()
        return amount, note