from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from services.inventory_stats import InventoryStats
import matplotlib
matplotlib.use('Qt5Agg')  
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
class OverviewPage(QWidget):

    def __init__(self):
        super().__init__()
        self.inventory_stats = InventoryStats()
        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # ================= TITLE =================
        title = QLabel("📊 Inventory Overview")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")
        layout.addWidget(title)

        # ================= CARDS ROW =================
        cards_row = QHBoxLayout()
        cards_row.setSpacing(15)

        cards_row.addWidget(self.card("عدد جميع العناصر", str(self.inventory_stats.get_total_items())))
        cards_row.addWidget(self.card("جميع الكميات الموجودة", str(self.inventory_stats.get_total_quantity())))
        cards_row.addWidget(self.card("عدد العناصر التي كميتها صفر", str(self.inventory_stats.get_low_stock())))
        cards_row.addWidget(self.card("عدد الاصناف الموجودة", str(self.inventory_stats.get_categories_count())))

        layout.addLayout(cards_row)

        # ================= CHARTS AREA =================
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(15)

        # Bar Chart
        self.bar_canvas = self.create_bar_chart()
        charts_layout.addWidget(self.bar_canvas)

        # Pie Chart
        self.pie_canvas = self.create_pie_chart()
        charts_layout.addWidget(self.pie_canvas)

        layout.addLayout(charts_layout)
    # ---------------- CARD ----------------
    def card(self, title, value):

        frame = QFrame()
        frame.setFixedHeight(110)
        frame.setStyleSheet("""
            background-color: #1F2937;
            border-radius: 12px;
        """)

        layout = QVBoxLayout(frame)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #9CA3AF; font-size: 12px;")

        lbl_value = QLabel(value)
        lbl_value.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_value)

        return frame
    
    # ------------------- charts -------------------
    def create_bar_chart(self):
        from services.chart_service import ChartService
        from matplotlib.figure import Figure

        items = ChartService.get_top_items_by_quantity(7)

        fig = Figure(figsize=(8, 5), dpi=110, facecolor='#1F2937')
        ax = fig.add_subplot(111)

        names = [item.name[:18] for item in items]   
        quantities = [item.quantity for item in items]

        bars = ax.bar(names, quantities, color='#00adb5', alpha=0.95, edgecolor='#00f5ff', linewidth=1.2)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                    f'{int(height)}', ha='center', va='bottom', 
                    color='white', fontsize=11, fontweight='bold')

        ax.set_title("أكثر الأصناف كمية", color='white', fontsize=16, pad=20)
        ax.set_ylabel("الكمية", color='#e5e7eb', fontsize=12)
        ax.set_xlabel("الأصناف", color='#e5e7eb', fontsize=12)

        ax.tick_params(axis='x', colors='#9ca3af', labelsize=10, rotation=45)
        ax.tick_params(axis='y', colors='#9ca3af', labelsize=10)

        ax.set_facecolor('#111827')
        ax.grid(True, axis='y', linestyle='--', alpha=0.2)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#4b5563')
        ax.spines['bottom'].set_color('#4b5563')

        fig.tight_layout()
        canvas = FigureCanvas(fig)
        canvas.setStyleSheet("""
            background-color: #1F2937; 
            border-radius: 12px;
            border: 1px solid #374151;
        """)
        return canvas


    def create_pie_chart(self):
        from services.chart_service import ChartService
        from matplotlib.figure import Figure

        data = ChartService.get_category_distribution()

        fig = Figure(figsize=(5.5, 4.5), dpi=110, facecolor='#1F2937')
        ax = fig.add_subplot(111)

        if not data or sum(row[1] for row in data) == 0:
            ax.text(0.5, 0.5, "لا توجد بيانات\nلعرض التوزيع", 
                   ha='center', va='center', color='#9ca3af', fontsize=14)
            ax.set_title("توزيع الأصناف حسب التصنيف", color='white', fontsize=14)
        else:
            categories = [row[0] or "غير مصنف" for row in data]
            values = [row[1] for row in data]

            colors = ['#00adb5', '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57']

            ax.pie(values, labels=categories, autopct='%1.1f%%', 
                   colors=colors[:len(values)], startangle=90, 
                   textprops={'color': 'white', 'fontsize': 10})

            ax.set_title("توزيع الأصناف حسب التصنيف", color='white', fontsize=14, pad=20)

        canvas = FigureCanvas(fig)
        canvas.setStyleSheet("""
            background-color: #1F2937; 
            border-radius: 12px;
            border: 1px solid #374151;
        """)
        return canvas