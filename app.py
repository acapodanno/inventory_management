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
from logs.logging_config import setup_logging
from service.report_service import ReportService    
def main():
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



if __name__ == "__main__":
    main()
