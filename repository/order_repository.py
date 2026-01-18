from model.order_model import OrderModel
class OrderRepository:
    def __init__(self, path):
        self.path = path

    def find_all(self):
        orders = {}
        with open(self.path, 'r') as file:
            next(file)
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 5:
                    orderId, orderDate, status, priority, userId = parts
                    orders[orderId] = OrderModel(
                        orderId,
                        orderDate,
                        status,
                        priority,
                        userId
                    )
        return orders
    def save(self, order):
        with open(self.path, 'a') as file:
            line = f"{order.orderId},{order.orderDate},{order.status},{order.priority},{order.userId}\n"
            file.write(line)