from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, QGroupBox
)
from PySide6.QtCore import Qt


class ReportUI(QWidget):
    def __init__(self, report_service, parent=None):
        super().__init__(parent)
        self.report_service = report_service

        root = QVBoxLayout(self)
        header = QHBoxLayout()
        self.title = QLabel("Daily Report")
        header.addWidget(self.title)

        header.addStretch(1)

        self.generate_btn = QPushButton("Generate today report")
        header.addWidget(self.generate_btn)

        root.addLayout(header)

        kpi_box = QGroupBox("Summary")
        kpi_layout = QHBoxLayout(kpi_box)

        self.total_orders_lbl = QLabel("Total orders: 0")
        self.completed_orders_lbl = QLabel("Completed: 0")
        self.pending_orders_lbl = QLabel("Pending: 0")

        for lbl in (self.total_orders_lbl, self.completed_orders_lbl, self.pending_orders_lbl):
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("font-size: 14px;")

        kpi_layout.addWidget(self.total_orders_lbl)
        kpi_layout.addWidget(self.completed_orders_lbl)
        kpi_layout.addWidget(self.pending_orders_lbl)

        root.addWidget(kpi_box)

        table_box = QGroupBox("Most Fulfilled Products")
        table_layout = QVBoxLayout(table_box)

        self.products_table = QTableWidget(0, 2)
        self.products_table.setHorizontalHeaderLabels(["productCode", "quantityFulfilled"])
        self.products_table.setSortingEnabled(True)

        table_layout.addWidget(self.products_table)
        root.addWidget(table_box)


        self.generate_btn.clicked.connect(self.generate_report)


    def generate_report(self):
        report = self.report_service.generated_daily_report()
        self.total_orders_lbl.setText(f"Total orders: {report.numberOrders}")
        self.completed_orders_lbl.setText(f"Completed: {report.numberOrderCompleted}")
        self.pending_orders_lbl.setText(f"Pending: {report.numberOrderPending}")

        self.render_products(report.productsMostFulfilled)
    def render_products(self, products):
        self.products_table.setSortingEnabled(False)
        self.products_table.clearContents()
        self.products_table.setRowCount(len(products))

        for r, (code, qty) in enumerate(products):
            self.products_table.setItem(r, 0, QTableWidgetItem(str(code)))
            self.products_table.setItem(r, 1, QTableWidgetItem(str(qty)))

        self.products_table.setSortingEnabled(True)
        self.products_table.resizeColumnsToContents()

    def reset_ui(self):
        self.total_orders_lbl.setText("Total orders: 0")
        self.completed_orders_lbl.setText("Completed: 0")
        self.pending_orders_lbl.setText("Pending: 0")
        self.products_table.setRowCount(0)