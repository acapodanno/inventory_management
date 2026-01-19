from service.order_service import OrderService
from service.order_product_service import OrderProductService
from service.product_service import ProductService
import uuid
from model.order_product_model import OrderProductModel
import logging
from constant.order_product_status import OrderProductStatus
from constant.order_status import OrderStatus
from constant.product_status import ProductStatus
class SendOrder:
    def __init__(self, order_service: OrderService, order_product_service: OrderProductService,product_service: ProductService):
        self.order_service = order_service
        self.order_product_service = order_product_service
        self.product_service = product_service
        self.logger = logging.getLogger(__name__)
    
    def send_order(self, order, product_lines):
        self.logger.info(f"Processing order {order.orderId} with product lines: {product_lines}")
        order_products = []
        for line in product_lines:
            productCode = line['productCode']
            quantity = line['quantity']
            order_product = self._process_product_line(productCode, quantity,order.orderId)
            order_products.append(order_product)
        order.status = self._determinate_order_status_from_product_lines(order_products)
        self.order_service.add_order(order)

    def _determinate_order_status_from_product_lines(self, order_products):
        all_fulfilled = all(op.status == OrderProductStatus.FULFILLED for op in order_products)
        all_unfulfilled = all(op.status == OrderProductStatus.UNFULFILLED for op in order_products)
        if all_fulfilled:
            return OrderStatus.COMPLETED
        elif all_unfulfilled:
            return OrderStatus.PENDING
        else:
            return OrderStatus.PARTIALLY_COMPLETED

    def _process_product_line(self, productCode, quantity, orderId):
        products = self.product_service.get_all_products()
        product = products.get(productCode)
        if not product:
            self.logger.warning(f"Product {productCode} not found.")
            raise Exception(f"Product not found.")
        if product and product.status == ProductStatus.ACTIVE and product.initialStock >= quantity:
            order_product = OrderProductModel(
                orderId=orderId,
                productCode=productCode,
                quantityOrdered=quantity,
                quantityFulfilled=quantity,
                status= OrderProductStatus.FULFILLED
            )
            self.order_product_service.add_order_product(order_product)
            product.initialStock -= quantity
            self.product_service.update_product(product)
            return order_product
        elif product and product.status == ProductStatus.ACTIVE and 0 < product.initialStock < quantity:
            order_product = OrderProductModel(
                orderId=orderId,
                productCode=productCode,
                quantityOrdered=quantity,
                quantityFulfilled=product.initialStock,
                status=OrderProductStatus.PARTIALLY_FULFILLED
            )
            self.order_product_service.add_order_product(order_product)
            product.initialStock = 0
            self.product_service.update_product(product)
            return order_product
        else:
            order_product = OrderProductModel(
                orderId=orderId,
                productCode=productCode,
                quantityOrdered=quantity,
                quantityFulfilled=0,
                status=OrderProductStatus.UNFULFILLED
            )
            self.order_product_service.add_order_product(order_product)
            return order_product