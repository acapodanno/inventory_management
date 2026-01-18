class OrderProductModel:
    def __init__(self, orderId, productCode, quantityOrdered, quantityFulfilled, status):
        self.orderId = orderId
        self.productCode = productCode
        self.quantityOrdered = quantityOrdered
        self.quantityFulfilled = quantityFulfilled
        self.status = status

    def __str__(self):
        return f"OrderProductModel({self.orderId}, {self.productCode}, {self.quantityOrdered}, {self.quantityFulfilled}, {self.status})"

    def __repr__(self):
        return self.__str__()