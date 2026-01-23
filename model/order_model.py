class OrderModel:
    """Model representing an order."""
    def __init__(self, orderId, orderDate, status,priority, userId):
        self.orderId = orderId
        self.orderDate = orderDate
        self.status = status
        self.priority = priority
        self.userId = userId
    
    def __str__(self):
        """ String representation for debugging."""    
        return f"OrderModel({self.orderId}, {self.orderDate}, {self.status}, {self.priority}, {self.userId})"
    
    def __repr__(self):
        """ Representation method."""
        return self.__str__()    