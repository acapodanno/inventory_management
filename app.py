import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from service.product_service import ProductService
from service.order_service import OrderService
from repository.order_repository import OrderRepository
from repository.product_repository import ProductRepository
from service.send_order import SendOrder
from service.order_product_service import OrderProductService
from repository.order_product_repository import OrderProductRepository
from util.logging_config import setup_logging
from service.report_service import ReportService   
from util.csv_management import ensure_csv_file_exists,ensure_directory_exists


def main():
    _intiialize_cvs_files()
    setup_logging()
    app = QApplication(sys.argv)
    productService = ProductService(ProductRepository('dummy_data/products.csv'))
    orderService = OrderService(OrderRepository('dummy_data/orders.csv'))
    orderProductService = OrderProductService(OrderProductRepository('dummy_data/order_products.csv'))
    sendOrderService = SendOrder(orderService, orderProductService, productService)
    reportService = ReportService(orderService, productService, orderProductService)
    w = MainWindow(product_service=productService, order_service=orderService, send_order=sendOrderService, order_product_service=orderProductService,report_service=reportService)
    w.show()
    sys.exit(app.exec())
def _intiialize_cvs_files():
    ensure_directory_exists('dummy_data')
    csv_headers = {
        'dummy_data/products.csv': ['productCode', 'name', 'category', 'initialStock', 'reorderPoint', 'unitOfMeasure', 'status', 'maxStock'],
        'dummy_data/orders.csv': ['orderId', 'orderDate', 'status', 'priority', 'userId'],
        'dummy_data/order_products.csv': ['orderId', 'productCode', 'quantity_ordered', 'quantity_fulfilled', 'status'],
        'dummy_data/logs.csv': ['timestamp', 'level', 'name', 'message']
    }
    for file_path, headers in csv_headers.items():
        ensure_csv_file_exists(file_path, headers)

if __name__ == "__main__":
    main()
