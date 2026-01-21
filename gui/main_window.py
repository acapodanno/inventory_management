import sys
from PySide6.QtWidgets import (
     QMainWindow, QWidget, QVBoxLayout,QTabWidget,QLabel
)
from gui.product.product_ui import ProductUI
from gui.order.order_ui import OrderUI
from gui.report.report_ui import ReportUI
import os
from dotenv import load_dotenv
class MainWindow(QMainWindow):
    def __init__(self,product_service, order_service, send_order, order_product_service, report_service, parent=None):
        super().__init__()
        load_dotenv()
        title = os.environ.get("TITLE")
        self.setWindowTitle(title)
        self.resize(900, 600)
        root = QWidget()
        self.setCentralWidget(root)
        main_layout = QVBoxLayout(root)
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        self.product_ui = ProductUI(product_service)
        self.order_ui = OrderUI(send_order, order_service, order_product_service)
        self.report_ui = ReportUI(report_service)
        products_tab = self._create_tab_widget(self.product_ui)
        orders_tab = self._create_tab_widget(self.order_ui)
        reports_tab = self._create_tab_widget(self.report_ui)
        self._add_tab([
            (orders_tab, "Orders"),
            (products_tab, "Products"),
            (reports_tab, "Reports")
        ])
        self.tabs.currentChanged.connect(self._on_tab_changed)

    def _on_tab_changed(self, index):
        if index == 0:
            self.product_ui.reload_data()
        elif index == 1:
            self.order_ui.reload_orders()
        elif index == 2:
            self.report_ui.reset_ui()

    def _create_tab_widget(self, widget):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.addWidget(widget)
        return tab
    
    def _add_tab(self, widgets):
        for widget, title in widgets:
            self.tabs.addTab(widget, title)