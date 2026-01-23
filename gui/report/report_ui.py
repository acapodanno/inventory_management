from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, QGroupBox
)
from PySide6.QtCore import Qt
from util.generate_excel import generate_excel

class ReportUI(QWidget):
    """UI component for generating and displaying daily reports."""
    _header_title = "Daily Report"
    _btn_generate_excel_title = "Generate Excel Report"
    _btn_generate_report_title = "Generate today report"
    def __init__(self, report_service, parent=None):
        super().__init__(parent)
        self.report_service = report_service

        root = QVBoxLayout(self)
        header = QHBoxLayout()
        self.title = QLabel(self._header_title)
        header.addWidget(self.title)

        header.addStretch(1)
        self.generate_excel_btn = QPushButton(self._btn_generate_excel_title)
        self.generate_btn = QPushButton(self._btn_generate_report_title)
        header.addWidget(self.generate_btn)
        header.addWidget(self.generate_excel_btn)
        root.addLayout(header)

        kpi_box = QGroupBox("Summary")
        kpi_layout = QHBoxLayout(kpi_box)

        self.total_orders_lbl = QLabel("Total orders: 0")
        self.completed_orders_lbl = QLabel("Completed: 0")
        self.pending_orders_lbl = QLabel("Pending: 0")

        for lbl in (self.total_orders_lbl, self.completed_orders_lbl, self.pending_orders_lbl):
            lbl.setAlignment(Qt.AlignCenter)

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


        self.generate_btn.clicked.connect(self._generate_report)
        self.generate_excel_btn.clicked.connect(self._generate_excel_report)
    def _generate_excel_report(self):
        """ Generate and save the daily report as an Excel file."""
        report = self.report_service.generated_daily_report()
        generate_excel({
            "dailyReport": [report.numberOrders,
                            report.numberOrderCompleted,
                            report.numberOrderPending],
            "productsMostFulfilled": report.productsMostFulfilled
        }, "daily_report.xls")
    def _generate_report(self):
        """ Generate and display the daily report in the UI."""
        report = self.report_service.generated_daily_report()
        self.total_orders_lbl.setText(f"Total orders: {report.numberOrders}")
        self.completed_orders_lbl.setText(f"Completed: {report.numberOrderCompleted}")
        self.pending_orders_lbl.setText(f"Pending: {report.numberOrderPending}")

        self._render_products(report.productsMostFulfilled)
    def _render_products(self, products):
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