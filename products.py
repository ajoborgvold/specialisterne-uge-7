import csv

class Product:
    def __init__(self, product_id, name, description, category, price, stock):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.category = category
        self.price = price
        self.stock = stock
    
    def __str__(self):
        return f"\nId: {self.product_id}\nName: {self.name}\nDescription: {self.description}\nCategory: {self.category}\nPrice: {self.price}\nStock: {self.stock}\nOn sale: No"
    
    def show_price(self):
        return self.price
    
    def show_stock(self):
        return self.stock
    
    def update_stock(self, stock_change):
        self.stock += stock_change

class ProductOnSale(Product):
    def __init__(self, product_id, name, description, category, price, stock, discount):
        super().__init__(product_id, name, description, category, price, stock)
        self.discount = discount
        
    def __str__(self):
        return f"\nId: {self.product_id}\nName: {self.name}\nDescription: {self.description}\nCategory: {self.category}\nPrice: {self.price}\nStock: {self.stock}\nOn sale: Yes"
    
    def show_price(self):
        discounted_price = round(self.price - (self.price * self.discount / 100), 2)
        return discounted_price

class Factory:
    def __init__(self, catalogue):
        self.catalogue = catalogue
        self.next_product_id = 1
    
    def _generate_unique_id(self):
        product_id = self.next_product_id
        self.next_product_id += 1
        return product_id
    
    def generate_fake_product(self, row):
        product_id = self._generate_unique_id()
        price = float(row["Price"])
        stock = int(row["Stock"])
        self.catalogue.add_product(Product(product_id, row["Name"], row["Description"], row["Category"], price, stock))
    
    def create_new_product(self, name, description, category, price, stock, **kwargs):
        product_id = self._generate_unique_id()
        if "discount" in kwargs and isinstance(kwargs["discount"], (int, float)) and 0 < kwargs["discount"] < 100:
            discount = kwargs["discount"]
            self.catalogue.add_product(ProductOnSale(product_id, name, description, category, price, stock, discount))
        else:
            self.catalogue.add_product(Product(product_id, name, description, category, price, stock))

class Catalogue:
    def __init__(self):
        self.products = []
    
    def add_product(self, new_product):
        for product in self.products:
            if product.name.lower() == new_product.name.lower() or product.description.lower() == new_product.description.lower():
                print(f"A product with the name {new_product.name} or the description {new_product.description} already exists in the catalogue.")
                return
        self.products.append(new_product)
    
    def delete_product(self, product_id):
        for product in self.products:
            if product.product_id == product_id:
                self.products.remove(product)
                print(f"The product with the name {product.name} and the id {product_id} was successfully removed.")
                return True
        return False
    
    def get_unique_categories(self):
        unique_categories = {product.category for product in self.products}
        return [{"id": index, "category": category} for index, category in enumerate(unique_categories, start=1)]
    
    def search_product(self, query_type, query_value):
        validation_error = self._validate_query(query_type, query_value)
        if validation_error:
            return validation_error
        
        if query_type == "id":
            return self._search_product_by_id(query_value)
        elif query_type == "name":
            return self._search_product_by_name(query_value)
        elif query_type == "category":
            return self._search_product_by_category(query_value)
        elif query_type == "discount":
            return self._search_product_by_discount(query_value)
        else:
            return f"Invalid query type: {query_type}. Please provide a valid query type (id, name or category)."
    
    def _validate_query(self, query_type, query_value):
        if query_type == "id":
            try:
                int(query_value)
            except ValueError:
                return f"Invalid product {query_type}: {query_value}. Please provide a valid integer ID."
        elif query_type == "name" and not isinstance(query_value, str):
            return f"Invalid product {query_type}: {query_value}. Please provide a valid string."
        elif query_type == "category" and not isinstance(query_value, str):
            return f"Invalid product {query_type}: {query_value}. Please provide a valid string."
        elif query_type == "discount" and not isinstance(query_value, bool):
            return f"Invalid discount query: {query_value}. Please provide a valid boolean (True or False)."
        else:
            return None
    
    def _search_product_by_id(self, product_id):
        for product in self.products:
            if product.product_id == int(product_id):
                return product
                
        return f"No product with the id {product_id} in the catalogue."
    
    def _search_product_by_name(self, name):
        for product in self.products:
            if product.name.lower() == name.lower():
                return product
                
        return f"No product with the name {name} in the catalogue."
    
    def _search_product_by_category(self, category):
        matching_products = [str(product) for product in self.products if product.category.lower() == category.lower()]
        
        if matching_products:
            return "\n".join(matching_products)
        else:
            return f"No products in the category: {category}"
    
    def _search_product_by_discount(self, has_discount):
        if has_discount:
            discounted_products = [str(product) for product in self.products if isinstance(product, ProductOnSale)]
        else:
            discounted_products = [str(product) for product in self.products if not isinstance(product, ProductOnSale)]
        
        if discounted_products:
            return "\n".join(discounted_products)
        else:
            if has_discount:
                return "No discounted products found."
            else:
                return "No products without discount found."
    
    def show_total_stock(self):
        stock_list = []
        
        for product in self.products:
            product_stock = {product.name: product.stock}
            stock_list.append(product_stock)
        
        return f"Unique products in the catalogue: {len(self.products)}.\nStock for each unique product:\n{stock_list}"

catalogue = Catalogue()
factory = Factory(catalogue)

def generate_products_from_csv(filepath):
    with open(filepath) as file:
        reader = csv.DictReader(file)
        for row in reader:
            factory.generate_fake_product(row)

generate_products_from_csv("fake_products.csv")

all_categories = catalogue.get_unique_categories()
# print(all_categories)


factory.create_new_product("Speaker", "High-quality audio speaker", "Electronics", 99.99, 50, discount=10)
# print(product_on_sale.get_discounted_price())

# search_result = catalogue.search_product("discount", True)
# print(search_result)


# catalogue.delete_product(8)

for product in catalogue.products:
    print(product)
    print("Price", product.show_price())

# print(catalogue.show_total_stock())
