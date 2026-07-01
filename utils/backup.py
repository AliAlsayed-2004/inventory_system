import shutil
from datetime import datetime
from pathlib import Path
from PySide6.QtWidgets import QFileDialog, QMessageBox


def create_backup(parent=None):
    db_path = Path("inventory.db")
    
    if not db_path.exists():
        QMessageBox.warning(parent, "خطأ", "ملف قاعدة البيانات غير موجود!")
        return False

    # اسم الملف مع التاريخ
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f"inventory_backup_{timestamp}.db"
    
    # اختيار مكان الحفظ
    save_path, _ = QFileDialog.getSaveFileName(
        parent,
        "حفظ النسخة الاحتياطية",
        backup_filename,
        "Database Files (*.db)"
    )
    
    if save_path:
        try:
            shutil.copy2(db_path, save_path)
            QMessageBox.information(parent, "نجاح", 
                                  f"تم إنشاء النسخة الاحتياطية بنجاح!\n\n{save_path}")
            return True
        except Exception as e:
            QMessageBox.critical(parent, "خطأ", f"فشل في إنشاء النسخة:\n{str(e)}")
            return False
    return False