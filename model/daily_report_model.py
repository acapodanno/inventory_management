class DailyReportModel:
    """Model representing a daily report."""
    def __init__(self, numberOrders,numberOrderCompleted,numberOrderPending,productsMostFulfilled):
        self.numberOrders = numberOrders
        self.numberOrderCompleted = numberOrderCompleted
        self.numberOrderPending = numberOrderPending
        self.productsMostFulfilled = productsMostFulfilled
        