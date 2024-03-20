import csv

class Book:
    def __init__(self, product_id, **kwargs):
        self.product_id = product_id
        self.title = kwargs["title"]
        self.author = kwargs["author"]
        self.description = kwargs["description"]
        self.category = kwargs["category"]
        self.medium = kwargs["medium"]
        self.audience = kwargs["audience"]
        self.size = kwargs["size"]
        self.price = kwargs["price"]
        self.stock = kwargs["stock"]
    
    def __str__(self):
        return f"\nId: {self.product_id}\nTitle: {self.title}\nAuthor(s): {self.author}\nCategory: {self.category}\nMedium: {self.medium}\nAudience: {self.audience}\nPrice: {self.price}\nStock: {self.stock}"
    
    def show_book_size(self):
        return f"The book {self.title} has a size of {self.size}."
    
    def show_price(self):
        return self.price
    
    def show_stock(self):
        return self.stock
    
    def update_stock(self, stock_change):
        self.stock += stock_change

class PrintedBook(Book):
    def __init__(self, product_id, **kwargs):
        super().__init__(product_id, **kwargs)
        self.title = kwargs["title"]
        self.num_pages = kwargs["size"]
    
    def show_book_size(self):
        return f"The book '{self.title}' has a size of {self.num_pages} pages."

class EBook(Book):
    def __init__(self, product_id, **kwargs):
        super().__init__(product_id, **kwargs)
        self.title = kwargs["title"]
        self.byte_size = kwargs["size"]
    
    def show_book_size(self):
        return f"The book '{self.title}' has a size of {self.byte_size} KB."

class Audiobook(Book):
    def __init__(self, product_id, **kwargs):
        super().__init__(product_id, **kwargs)
        self.title = kwargs["title"]
        self.length_minutes = kwargs["size"]
        
    def show_book_size(self):
        return f"The book '{self.title}' has a length of {self.length_minutes} minutes."

class Factory:
    def __init__(self, catalogue):
        self.catalogue = catalogue
        self.next_product_id = 1
    
    def _generate_unique_id(self):
        product_id = self.next_product_id
        self.next_product_id += 1
        return product_id
    
    def generate_fake_product(self, row):     
        common_args = {
            "title": row["title"],
            "author": row["author"],
            "description": row["description"],
            "category": row["category"],
            "medium": row["medium"],
            "audience": row["audience"],
            "size": row["size"],
            "price": float(row["price"]),
            "stock": int(row["stock"])
        }
        self.create_new_product(**common_args)
    
    def create_new_product(self, **kwargs):
        medium = kwargs["medium"].lower()
        product_id = self._generate_unique_id()
        if medium == "printed":
            self.catalogue.add_product(PrintedBook(product_id, **kwargs))
        elif medium == "audiobook":
            self.catalogue.add_product(Audiobook(product_id, **kwargs))
        elif medium == "e-book":
            self.catalogue.add_product(EBook(product_id, **kwargs))

class Catalogue:
    def __init__(self):
        self.products = []
    
    def add_product(self, new_product):
        for product in self.products:
            if product.title.lower() == new_product.title.lower() and product.author.lower() == new_product.author.lower():
                print(f"The book {new_product.title} by {new_product.author} already exists in the catalogue.")
                return
        self.products.append(new_product)
    
    def delete_product(self, product_id):
        for product in self.products:
            if product.product_id == product_id:
                self.products.remove(product)
                print(f"The product with the title {product.title} and the id {product_id} was successfully removed.")
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
        elif query_type == "title":
            return self._search_product_by_title(query_value)
        elif query_type == "category":
            return self._search_product_by_category(query_value)
        elif query_type == "medium":
            return self._search_product_by_medium(query_value)
        else:
            return f"Invalid query type: {query_type}. Please provide a valid query type (id, name or category)."
    
    def _validate_query(self, query_type, query_value):
        if query_type == "id":
            try:
                int(query_value)
            except ValueError:
                return f"Invalid product {query_type}: {query_value}. Please provide a valid integer ID."
        elif query_type == "title" and not isinstance(query_value, str):
            return f"Invalid product {query_type}: {query_value}. Please provide a valid string."
        elif query_type == "category" and query_value.lower() not in ["fiction", "non-fiction"]:
            return f"Invalid product {query_type}: {query_value}. Please provide a valid string."
        elif query_type == "medium" and query_value.lower() not in ["printed", "audiobook", "e-book"]:
            return f"Invalid product {query_type}: {query_value}. Please provide a valid string."
        else:
            return None
    
    def _search_product_by_id(self, product_id):
        for product in self.products:
            if product.product_id == int(product_id):
                return product
                
        return f"No book with the id {product_id} in the catalogue."
    
    def _search_product_by_title(self, title):
        for product in self.products:
            if product.title.lower() == title.lower():
                return product
                
        return f"No book with the title {title} in the catalogue."
    
    def _search_product_by_category(self, category):
        matching_products = [str(product) for product in self.products if product.category.lower() == category.lower()]
        
        if matching_products:
            return "\n".join(matching_products)
        else:
            return f"No books in the category {category} in the catalogue."
    
    def _search_product_by_medium(self, medium):
        matching_products = [str(product) for product in self.products if product.medium.lower() == medium.lower()]
        
        if matching_products:
            return "\n".join(matching_products)
        else:
            return f"No books with the medium {medium} in the catalogue."
    
    def show_total_stock(self):
        stock_list = []
        
        for product in self.products:
            product_stock = {product.title: product.stock}
            stock_list.append(product_stock)
        
        return f"Unique products in the catalogue: {len(self.products)}.\nStock for each unique product:\n{stock_list}"

catalogue = Catalogue()
factory = Factory(catalogue)

def generate_products_from_csv(filepath):
    with open(filepath) as file:
        reader = csv.DictReader(file)
        for row in reader:
            factory.generate_fake_product(row)


def add_new_product():
    while True:
        print("Add new books to the book catalogue.")
        print("Options:\n1) Add books from a data file\n2) Enter new data\n3) Quit the menu.")
        option_selection = input("Enter your selection (1, 2 or q):\n").strip()
        
        if option_selection == "1":
            generate_products_from_csv("books_data.csv")
            print("25 books added.")
            submenu_selection = input("Enter p to print the books or q to quit the menu:\n").strip().lower()
            
            if submenu_selection == "p":
                for product in catalogue.products:
                    print(product)
                print()
                local_selection = input("Enter r to return to the main menu or q to quit the menu:\n").strip().lower()
                if local_selection == "r":
                    print()
                    continue
                elif local_selection == "q":
                    print("Quitting the menu.")
                    break
                else:
                    print(f"Invalid selection: {local_selection}. Returning to main menu.")
                    continue
            elif submenu_selection == "q":
                break
            else:
                print(f"Invalid selection: {submenu_selection}. Returning to main menu.")
                continue
            
        elif option_selection == "2":            
            valid_category = False
            valid_medium = False
            
            
            print("Enter new data to add a book to the catalogue.")
            title = input("Enter the book's title:\n").strip()
            author = input("Enter the author(s):\n").strip()
            description = input("Enter a description of the book:\n").strip()
            
            while not valid_category:
                category = input("Select a category: f for fiction and n for non-fiction:\n").strip().lower()
                if category in ["f", "n"]:
                    valid_category = True
                    continue
                else:
                    print("Invalid selection. Please try again.")
                
            while not valid_medium:
                medium = input("Select a medium: p for printed, a for audio and e for e-book:\n").strip().lower()
                if medium in ["p", "a", "e"]:
                    valid_medium = True
                    continue
                else:
                    print("Invalid selection. Please try again.\n")
                
            audience = input("Enter the target audience, e.g. children, young adults or adults:\n").strip()
            size = input("Enter the size, e.g. number of pages (printed books), length in minutes (audiobooks) or byte size in KB (e-books):\n").strip()
            price = round(float(input("Enter the price:\n").strip()), 2)
            stock = int(input("Enter the current stock, i.e. how many copies you're adding:\n").strip())
            
            
            args = {
                "title": title,
                "author": author,
                "description": description,
                "category": "fiction" if category == "f" else "non-fiction",
                "medium": "printed" if medium == "p" else "audiobook" if medium == "a" else "e-book",
                "audience": audience,
                "size": size,
                "price": price,
                "stock": stock
            }
            
            print(args)
            
            submenu_selection = input("Enter r to return to main menu, q to quit the menu:\n")
            
            if submenu_selection == "r":
                print("Returning to main menu.")
                continue
            elif submenu_selection == "q":
                print("Quitting the menu.")
                break
            else:
                print("Invalid selection. Returning to main menu.")
                continue
            
            
        elif option_selection == "q":
            print(f"Quitting the menu.")
            break
        else:
            print(f"Invalid selection. Please try again.")

add_new_product()

def search_catalogue():
    print("Search for a book in the catalogue")

search_catalogue()

# all_categories = catalogue.get_unique_categories()
# print(all_categories)


factory.create_new_product(
    title="Noget der hjælper",
    author="Mona Høvring",
    description="En bog om livet",
    category="Fiction",
    medium="Printed",
    audience="Adults",
    size=190,
    price=15.99,
    stock=50
)
# print(product_on_sale.get_discounted_price())

# search_result = catalogue.search_product("medium", "audiobook")
# print(search_result)


# catalogue.delete_product(1)

# for product in catalogue.products:
#     print(product)
#     print(product.show_book_size())

# print(catalogue.show_total_stock())

# print(catalogue.products[25])