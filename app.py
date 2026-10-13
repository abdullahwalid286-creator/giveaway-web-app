import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
    QGroupBox, QMessageBox, QHeaderView
)
from PyQt5.QtCore import Qt

class QuranCenterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.init_db_file()

    def init_db_file(self):
        # التأكد من إنشاء القاعدة عند التشغيل
        conn = sqlite3.connect("quran_center.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def initUI(self):
        self.setWindowTitle("نظام إدارة حلقات تحفيظ القرآن الكريم - النسخة الاحترافية")
        self.setGeometry(100, 100, 950, 600)
        self.setLayoutDirection(Qt.RightToLeft)

        # تصميم احترافي متناسق وجميل جداً
        self.setStyleSheet("""
            QMainWindow { background-color: #0f172a; color: #f8fafc; }
            QGroupBox { 
                font-weight: bold; font-size: 14px; color: #38bdf8; 
                border: 1px solid #1e293b; border-radius: 8px; 
                margin-top: 15px; padding-top: 18px; background-color: #1e293b;
            }
            QGroupBox::title { subcontrol-origin: margin; right: 15px; padding: 0 5px; }
            QPushButton { 
                background-color: #0284c7; color: white; font-weight: bold; 
                font-size: 13px; border-radius: 6px; padding: 8px 22px; 
            }
            QPushButton:hover { background-color: #0369a1; }
            QLineEdit { 
                background-color: #0f172a; color: #ffffff; 
                border: 1px solid #334155; border-radius: 6px; padding: 8px; font-size: 13px; 
            }
            QTableWidget { 
                background-color: #1e293b; color: #f8fafc; 
                gridline-color: #334155; border: 1px solid #334155; border-radius: 6px; 
            }
            QHeaderView::section { 
                background-color: #0f172a; color: #38bdf8; 
                padding: 8px; border: none; font-weight: bold; font-size: 13px;
            }
            QLabel { color: #cbd5e1; font-size: 13px; font-weight: bold; }
        """)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # عنوان رئيسي للبرنامج
        title_label = QLabel("📖 لوحة تحكم مركز تحفيظ القرآن الكريم")
        title_label.setStyleSheet("font-size: 18px; color: #38bdf8; margin-bottom: 5px;")
        main_layout.addWidget(title_label)

        # قسم إضافة طالب جديد
        group_add = QGroupBox("إضافة طالب جديد للحلقة")
        add_layout = QHBoxLayout(group_add)
        add_layout.setSpacing(12)

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("اكتب اسم الطالب هنا...")
        
        btn_add = QPushButton("إضافة الطالب وتثبيته")
        btn_add.clicked.connect(self.add_student)

        add_layout.addWidget(QLabel("اسم الطالب:"))
        add_layout.addWidget(self.input_name)
        add_layout.addWidget(btn_add)

        main_layout.addWidget(group_add)

        # قسم عرض قائمة الطلاب المسجلين
        group_list = QGroupBox("قائمة الطلاب المسجلين في النظام")
        list_layout = QVBoxLayout(group_list)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        # ترتيب الأعمدة المضبوط: اليمين هو المعرف، الوسط الاسم، اليسار التاريخ
        self.table.setHorizontalHeaderLabels(["المعرف (ID)", "اسم الطالب", "تاريخ التسجيل"])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        list_layout.addWidget(self.table)
        main_layout.addWidget(group_list)

        # تحميل البيانات المحفوظة مسبقاً
        self.load_students()

    def get_db_connection(self):
        return sqlite3.connect("quran_center.db")

    def load_students(self):
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, created_at FROM students")
            rows = cursor.fetchall()
            conn.close()

            self.table.setRowCount(0)
            for row_idx, row_data in enumerate(rows):
                self.table.insertRow(row_idx)
                for col_idx, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(row_idx, col_idx, item)
        except Exception as e:
            print(f"خطأ في التحميل: {e}")

    def add_student(self):
        name = self.input_name.text().strip()
        if not name:
            QMessageBox.warning(self, "تنبيه هام", "يرجى كتابة اسم الطالب أولاً قبل الحفظ!")
            return

        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students (name) VALUES (?)", (name,))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "عملية ناجحة", f"تم حفظ الطالب ({name}) في قاعدة البيانات بنجاح!")
            self.input_name.clear()
            self.load_students() # تحديث الجدول فورا ليظهر الطالب الجديد
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء الحفظ: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuranCenterApp()
    window.show()
    sys.exit(app.exec_())