class DailyReportModel:
    def __init__(self, numberOrders,numberOrderCompleted,numberOrderPending,productsMostFulfilled):
        self.numberOrders = numberOrders
        self.numberOrderCompleted = numberOrderCompleted
        self.numberOrderPending = numberOrderPending
        self.productsMostFulfilled = productsMostFulfilled
        