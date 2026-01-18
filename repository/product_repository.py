from model.product_model import ProductModel
class ProductRepository:

    def __init__(self, path):
        self.path = path

    def find_all(self):
        products = {}
        with open(self.path, 'r') as file:
            next(file)
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 7:
                    productCode, name, category, initialStock, reorderPoint, unitOfMeasure, status = parts
                    products[productCode] = ProductModel(
                        productCode,
                        name,
                        category,
                        int(initialStock),
                        int(reorderPoint),
                        unitOfMeasure,
                        status
                    )
        return products
    
    def find_by_filter(self, **filters):
        all_products = self.find_all()
        filtered_products = {code: product for code, product in all_products.items() if self.match_filter(product, **filters)}
        return filtered_products
    
    def match_filter(self, product, **filters):
        for key, value in filters.items():
            if not hasattr(product, key) or getattr(product, key) != value:
                return False
        return True
    def save(self, product):
        with open(self.path, 'a') as file:
            line = f"{product.productCode},{product.name},{product.category},{product.initialStock},{product.reorderPoint},{product.unitOfMeasure},{product.status}\n"
            file.write(line)

    def update(self, product):
        products = self.find_all()
        products[product.productCode] = product
        with open(self.path, 'w') as file:
            file.write("productCode,name,category,initialStock,reorderPoint,unitOfMeasure,status\n")  # Write header
            for p in products.values():
                line = f"{p.productCode},{p.name},{p.category},{p.initialStock},{p.reorderPoint},{p.unitOfMeasure},{p.status}\n"
                file.write(line)