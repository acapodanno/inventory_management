import logging 
class OrderService:
    def __init__(self, order_repository):
        self.order_repository = order_repository
        self.logger = logging.getLogger(__name__)

    def get_all_orders(self):
        self.logger.info("Fetching all orders")
        return self.order_repository.find_all()
    
    def add_order(self, order):
        self.logger.info(f"Adding new order: {order}")
        return self.order_repository.save(order)
    