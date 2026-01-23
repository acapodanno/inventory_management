class OrderProductService:
    """Service layer for managing order products."""
    def __init__(self, order_product_repository):
        self.order_product_repository = order_product_repository
    """CRUD operations for order products."""
    def get_all_order_products(self):
        """ Retrieve all order products."""
        return self.order_product_repository.find_all()
    
    def add_order_product(self, order_product):
        """ Add a new order product."""
        return self.order_product_repository.save(order_product)
    
    def get_order_products_by_order_id(self, orderId):
        """ Retrieve order products by order ID."""
        all_order_products = self.order_product_repository.find_all()
        filtered_order_products = {
            key: op for key, op in all_order_products.items() if op.orderId == orderId
        }
        return filtered_order_products
    
    def save_order_product(self, order_product):
        """ Delete an order product by ID."""
        return self.order_product_repository.save(order_product)
    
    def update_order_product(self, order_product):
        """ Update an existing order product."""
        return self.order_product_repository.update(order_product)