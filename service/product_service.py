import logging
class ProductService:
    def __init__(self, repository):
        self.repository = repository
        self.logger = logging.getLogger(__name__)


    def get_all_products(self):
        self.logger.info("Fetching all products")
        return self.repository.find_all()

    def get_products_by_filter(self, **filters):
        self.logger.info(f"Fetching products with filters: {filters}")
        return self.repository.find_by_filter(**filters)

    def add_product(self, product):
        self.logger.info(f"Adding new product: {product}")
        return self.repository.save(product)
    
    def update_product(self, product):
        self.logger.info(f"Updating product: {product}")
        return self.repository.update(product)