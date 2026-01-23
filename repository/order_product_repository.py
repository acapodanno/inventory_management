from model.order_product_model import OrderProductModel
class OrderProductRepository:
    """Repository layer for managing order products in CSV storage."""
    def __init__(self, path):
        self.path = path
    def find_all(self):
        """ Retrieve all order products."""
        order_products = {}
        with open(self.path, 'r') as file:
            next(file) 
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 5:
                    orderId, productCode, quantityOrdered, quantityFulfilled, status = parts
                    order_products_key = (orderId, productCode)
                    order_products[order_products_key] = OrderProductModel(
                        orderId,
                        productCode,
                        quantityOrdered,
                        quantityFulfilled,
                        status
                    )
        return order_products
    
    def save(self, order_product):
        """ Save a new order product."""
        with open(self.path, 'a') as file:
            line = f"{order_product.orderId},{order_product.productCode},{order_product.quantityOrdered},{order_product.quantityFulfilled},{order_product.status}\n"
            file.write(line)
           
    def update(self, order_product):
        """ Update an existing order product."""
        order_products = self.find_all()
        order_products_key = (order_product.orderId, order_product.productCode)
        order_products[order_products_key] = order_product
        with open(self.path, 'w') as file:
            for op in order_products.values():
                line = f"{op.orderId},{op.productCode},{op.quantityOrdered},{op.quantityFulfilled},{op.status}\n"
                file.write(line)