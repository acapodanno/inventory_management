from constant.order_status import OrderStatus
from datetime import datetime
from model.daily_report_model import DailyReportModel
class ReportService:
    def __init__(self, order_service, product_service,order_product_service):
        self.order_service = order_service
        self.product_service = product_service
        self.order_product_service = order_product_service

    def generated_daily_report(self):
        orders = self.order_service.get_all_orders()
        products = self.product_service.get_all_products()
        order_products = self.order_product_service.get_all_order_products()
        today = datetime.now().date()
        report = DailyReportModel(0,0,0,[])
        report.numberOrders = len(orders)
        report.numberOrderCompleted = sum(1 for order in orders.values() if order.status == OrderStatus.COMPLETED and datetime.strptime(order.orderDate, '%Y-%m-%d').date() == today)
        report.numberOrderPending = sum(1 for order in orders.values() if order.status == OrderStatus.PENDING and datetime.strptime(order.orderDate, '%Y-%m-%d').date() == today)
        product_fulfillment = {}
        for op in order_products.values():
            if op.productCode not in product_fulfillment:
                product_fulfillment[op.productCode] = 0
            product_fulfillment[op.productCode] += int(op.quantityFulfilled)
        most_fulfilled_products = sorted(product_fulfillment.items())[:5]
        report.productsMostFulfilled = [(products[code].name, qty) for code, qty in most_fulfilled_products if code in products]
        return report