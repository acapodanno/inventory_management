class OrderModel:
    def __init__(self, orderId, orderDate, status,priority, userId):
        self.orderId = orderId
        self.orderDate = orderDate
        self.status = status
        self.priority = priority
        self.userId = userId

    def __str__(self):
        return f"OrderModel({self.orderId}, {self.orderDate}, {self.status}, {self.priority}, {self.userId})"

    def __repr__(self):
        return self.__str__()    