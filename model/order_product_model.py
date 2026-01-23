class OrderProductModel:
    """Model representing a product line within an order."""
    def __init__(self, orderId, productCode, quantityOrdered, quantityFulfilled, status):
        self.orderId = orderId
        self.productCode = productCode
        self.quantityOrdered = quantityOrdered
        self.quantityFulfilled = quantityFulfilled
        self.status = status
    
    def __str__(self):
        """ String representation for debugging."""
        return f"OrderProductModel({self.orderId}, {self.productCode}, {self.quantityOrdered}, {self.quantityFulfilled}, {self.status})"
    
    def __repr__(self):
        """ Representation method."""
        return self.__str__()