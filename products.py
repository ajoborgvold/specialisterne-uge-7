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
        return f"Id: {self.product_id}\n Name: {self.name}\n Description: {self.description}\n Category: {self.category}\n Price: {self.price}\n Stock: {self.stock}"
    
    def show_stock(self):
        return self.stock
    
    def update_stock(self, stock_change):
        self.stock += stock_change

class Catalogue:
    def __init__(self):
        self.products = []
        self.next_product_id = 1

    def generate_unique_id(self):
        product_id = self.next_product_id
        self.next_product_id += 1
        return product_id
    
    def generate_fake_product(self, row):
        product_id = self.generate_unique_id()
        price = float(row["Price"])
        stock = int(row["Stock"])
        self.add_product(Product(product_id, row["Name"], row["Description"], row["Category"], price, stock))

    def create_new_product(self, name, description, category, price, stock):
        product_id = self.generate_unique_id()
        self.add_product(Product(product_id, name, description, category, price, stock))
    
    def add_product(self, product):
        self.products.append(product)
    
    def search_product_by_id(self, product_id):
        try:
            product_id = int(product_id)
        except ValueError:
            return f"Invalid product ID: {product_id}. Please provide a valid integer ID."
        
        for product in self.products:
            if product.product_id == product_id:
                return product
                
        return f"No product with the id {product_id} in the catalogue."
    
    def search_product_by_name(self, name):
        if not isinstance(name, str):
            return f"Invalid product name: {name}. Please provide a valid string."
        
        for product in self.products:
            if product.name.lower() == name.lower():
                return product
                
        return f"No product with the name {name} in the catalogue."
    
    def search_product_by_category(self, category):
        if not isinstance(category, str):
            return f"Invalid product category: {category}. Please provide a valid string."
        
        product_list = []
        
        for product in self.products:
            if product.category.lower() == category.lower():
                product_list.append(str(product))
            else:
                continue
        
        if product_list:
            return "\n".join(product_list)
        else:
            return f"No products in the category: {category}"
    
    def delete_product(self, product_id):
        for product in self.products:
            if product.product_id == product_id:
                self.products.remove(product)
                return True
        return False

catalogue = Catalogue()

with open("fake_products.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        catalogue.generate_fake_product(row)




# catalogue.create_new_product("Speaker", "High-quality audio speaker", "Electronics", 99.99, 50)

# for product in catalogue.products:
#     print(product)

# print(catalogue.search_product_by_name(True))
# print(catalogue.search_product_by_id(1))
# print(catalogue.search_product_by_category("electronics"))


# catalogue.delete_product(8)

# for product in catalogue.products:
#     print(product)