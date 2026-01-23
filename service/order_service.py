import logging 
class OrderService:
    """Service layer for managing orders."""
    def __init__(self, order_repository):
        self.order_repository = order_repository
        self.logger = logging.getLogger(__name__)
    """CRUD operations for orders."""
    
    def get_all_orders(self):
        """ Retrieve all orders."""
        self.logger.info("Fetching all orders")
        return self.order_repository.find_all()
    
    def add_order(self, order):
        """ Create a new order."""
        self.logger.info(f"Adding new order: {order}")
        return self.order_repository.save(order)
    