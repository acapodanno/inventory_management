from constant.order_status import OrderStatus
from datetime import datetime
from model.daily_report_model import DailyReportModel
import logging
class ReportService:
    def __init__(self, order_service, product_service,order_product_service):
        self.order_service = order_service
        self.product_service = product_service
        self.order_product_service = order_product_service
        self.logger = logging.getLogger(__name__)

    def generated_daily_report(self):
        self.logger.info("Generating daily report.")
        orders = self.order_service.get_all_orders()
        products = self.product_service.get_all_products()
        order_products = self.order_product_service.get_all_order_products()
        today = datetime.now().date()
        report = DailyReportModel(0,0,0,[])
        daily_orders = [order for order in orders.values() if datetime.strptime(order.orderDate, '%Y-%m-%d').date() == today]
        report.numberOrders = len(daily_orders)
        report.numberOrderCompleted = self._sum_order_for_status(daily_orders, OrderStatus.COMPLETED)
        report.numberOrderPending = self._sum_order_for_status(daily_orders, OrderStatus.PENDING)
        product_fulfillment = {}
        daily_order_ids = {order.orderId for order in daily_orders}
        order_products_result = [order_product for order_product in order_products.values() if order_product.orderId in daily_order_ids ]
        for op in order_products_result:
            if op.productCode not in product_fulfillment:
                product_fulfillment[op.productCode] = 0
            product_fulfillment[op.productCode] += int(op.quantityFulfilled)
        most_fulfilled_products = sorted(product_fulfillment.items())[:5]
        report.productsMostFulfilled = [(products[code].name, qty) for code, qty in most_fulfilled_products if code in products]
        return report
    
    def _sum_order_for_status(self, orders, status):
        return sum(1 for order in orders if order.status == status)