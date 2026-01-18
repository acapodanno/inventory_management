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
        title = os.environ.get("title")
        self.setWindowTitle(title)
        self.resize(900, 600)
        root = QWidget()
        self.setCentralWidget(root)
        main_layout = QVBoxLayout(root)
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        products_tab = QWidget()
        products_layout = QVBoxLayout(products_tab)
        self.product_ui = ProductUI(product_service)
        products_layout.addWidget(self.product_ui)
        
        orders_tab = QWidget()
        orders_layout = QVBoxLayout(orders_tab)
        self.order_ui = OrderUI(send_order, order_service, order_product_service)
        orders_layout.addWidget(self.order_ui)        
        reports_tab = QWidget()
        reports_layout = QVBoxLayout(reports_tab)
        self.report_ui = ReportUI(report_service)
        reports_layout.addWidget(self.report_ui)
        self.tabs.addTab(orders_tab, "Orders")
        self.tabs.addTab(products_tab, "Products")
        self.tabs.addTab(reports_tab, "Reports")
        self.tabs.currentChanged.connect(self._on_tab_changed)

    def _on_tab_changed(self, index):
        if index == 0:
            self.product_ui.reload_data()
        elif index == 1:
            self.order_ui.reload_orders()