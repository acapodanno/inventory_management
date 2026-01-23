from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QComboBox, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem
)
from gui.shared.custom_popup.custom_popup import CustomPopup
from gui.shared.custom_popup.custom_popop_level import CustomPopupLevel
class ProductUI(QWidget):
    """UI component for displaying and filtering products."""
    def __init__(self, product_service, parent=None):
        super().__init__(parent)
        self.product_service = product_service

        root = QVBoxLayout(self)
        filters = QHBoxLayout()
        root.addLayout(filters)

        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("e.g. P001")
        filters.addWidget(QLabel("Product code:"))
        filters.addWidget(self.code_input)

        self.category_combo = QComboBox()
        self.category_combo.addItems(["All"]) 
        filters.addWidget(QLabel("Category:"))
        filters.addWidget(self.category_combo)

        self.stock_threshold = QLineEdit()
        self.stock_threshold.setPlaceholderText("e.g. 50")
        filters.addWidget(QLabel("Stock ≤"))
        filters.addWidget(self.stock_threshold)

        self.apply_btn = QPushButton("Apply")
        self.refresh_btn = QPushButton("Refresh")
        filters.addWidget(self.apply_btn)
        filters.addWidget(self.refresh_btn)
        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels([
            "product_code", "name", "category",
            "initial_stock", "reorder_point",
            "unit_of_measure", "status"
        ])
        self.table.setSortingEnabled(True) 
        root.addWidget(self.table)

        self.apply_btn.clicked.connect(self.apply_filters)
        self.refresh_btn.clicked.connect(self.reload_data)

        self.products = {}
        self.reload_data()
    
    def reload_data(self):
        """ Reload product data from the service and update the UI."""
        self.products = self.product_service.get_all_products() 
        self._reload_categories()
        self.render_table(self.products.values())
    def _reload_categories(self):
        """ Reload product categories for the filter dropdown."""
        cats = sorted({p.category for p in self.products.values()})
        self.category_combo.blockSignals(True)
        self.category_combo.clear()
        self.category_combo.addItem("All")
        for c in cats:
            self.category_combo.addItem(c)
        self.category_combo.blockSignals(False)
    def apply_filters(self):
        """ Apply filters based on user input and update the table."""
        code = self.code_input.text().strip()
        cat = self.category_combo.currentText()
        thr_raw = self.stock_threshold.text().strip()

        thr = None
        if thr_raw:
            try:
                thr = int(thr_raw)
            except ValueError:
                thr = None

        filtered = []
        for p in self.products.values():
            if code and p.productCode != code:
                continue
            if cat != "All" and p.category != cat:
                continue
            if thr is not None and int(p.initialStock) > thr:
                continue
            filtered.append(p)
        if len(filtered) == 0:
            dlg = CustomPopup(CustomPopupLevel.INFO,"No products found!")
            dlg.exec()
            
        self.render_table(filtered)
    
    def render_table(self, rows):
        """ Render the given product rows in the table."""
        self.table.setRowCount(len(rows))
        self.table.setSortingEnabled(False)
        self.table.clearContents()
        for r, p in enumerate(rows):
            self.table.setItem(r, 0, QTableWidgetItem(getattr(p, "productCode", "")))
            self.table.setItem(r, 1, QTableWidgetItem(getattr(p, "name", "")))
            self.table.setItem(r, 2, QTableWidgetItem(getattr(p, "category", "")))
            self.table.setItem(r, 3, QTableWidgetItem(str(getattr(p, "initialStock", ""))))
            self.table.setItem(r, 4, QTableWidgetItem(str(getattr(p, "reorderPoint", ""))))
            self.table.setItem(r, 5, QTableWidgetItem(getattr(p, "unitOfMeasure", "")))
            self.table.setItem(r, 6, QTableWidgetItem(getattr(p, "status", "")))        
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.viewport().update()
        self.table.repaint()