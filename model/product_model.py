class ProductModel:
    # The constructor method to initialize new ProductModel instances
    def __init__(self,productCode,name,category,initialStock,reorderPoint,unitOfMeasure, status,maxStock):
        self.productCode = productCode
        self.name = name
        self.category = category
        self.initialStock = int(initialStock)
        self.reorderPoint = int(reorderPoint)
        self.maxStock = int(maxStock)
        self.unitOfMeasure = unitOfMeasure
        self.status = status
        
    def __str__(self):
        return f"ProductModel({self.productCode}, {self.name}, {self.category}, {self.initialStock}, {self.reorderPoint}, {self.unitOfMeasure}), {self.status})"
    def __repr__(self):
        return self.__str__()