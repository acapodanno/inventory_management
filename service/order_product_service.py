class OrderProductService:
    def __init__(self, order_product_repository):
        self.order_product_repository = order_product_repository
    def get_all_order_products(self):
        return self.order_product_repository.find_all()
    def add_order_product(self, order_product):
        return self.order_product_repository.save(order_product)
    def get_order_products_by_order_id(self, orderId):
        all_order_products = self.order_product_repository.find_all()
        filtered_order_products = {
            key: op for key, op in all_order_products.items() if op.orderId == orderId
        }
        return filtered_order_products
    def save_order_product(self, order_product):
        return self.order_product_repository.save(order_product)
    def update_order_product(self, order_product):
        return self.order_product_repository.update(order_product)