class Book:
    '''
    This is a parent class, that is used to create all shared attributes and methods on the book objects. The class is not itself used to directly create objects/instances; instead, child classes extend this parent class to create specialized types of books based on the medium.
    
    Polymorphism is demonstrated through the `show_book_size` method, which is overridden in the child classes (`PrintedBook`, `AudioBook`, `EBook`) to provide specific implementations based on the medium of the book.
    '''
    
    def __init__(self, book_id, **kwargs):
        self.book_id = book_id
        self.title = kwargs["title"]
        self.author = kwargs["author"]
        self.description = kwargs["description"]
        self.category = kwargs["category"]
        self.medium = kwargs["medium"]
        self.audience = kwargs["audience"]
        self.size = kwargs["size"]
        self.purchase_price = kwargs["purchase_price"]
        self.selling_price = kwargs["selling_price"]
        self.stock = kwargs["stock"]
    
    def __str__(self):
        return f"\nId: {self.book_id}\nTitle: {self.title}\nAuthor(s): {self.author}\nCategory: {self.category}\nMedium: {self.medium}\nStock: {self.stock}"
    
    def show_book_size(self):
        return f"The book {self.title} has a size of: {self.size}."
    
    def show_purchase_price(self):
        return f"Purchase price for the book {self.title}: {self.purchase_price}."
    
    def show_selling_price(self):
        return f"Selling price for the book {self.title}: {self.selling_price}."
    
    def show_stock(self):
        return f"Current stock for the book {self.title}: {self.stock}"
    
    def update_stock(self, stock_change):
        self.stock += stock_change

class PrintedBook(Book):
    '''
    This class is responsible for creating instances of printed books. Therefore, the show_book_size method will display the book_size as the number of pages in the printed book. All other attributes and methods are inherited from the Book parent class.
    '''
    def __init__(self, book_id, **kwargs):
        super().__init__(book_id, **kwargs)
        self.title = kwargs["title"]
        self.num_pages = kwargs["size"]
    
    def show_book_size(self):
        return f"The printed book '{self.title}' has {self.num_pages} pages."

class EBook(Book):
    '''
    This class is responsible for creating instances of e-books. Therefore, the show_book_size method will display the book_size as the digital byte size of the e-book file. All other attributes and methods are inherited from the Book parent class.
    '''
    
    def __init__(self, book_id, **kwargs):
        super().__init__(book_id, **kwargs)
        self.title = kwargs["title"]
        self.byte_size = kwargs["size"]
    
    def show_book_size(self):
        return f"The e-book '{self.title}' has a size of {self.byte_size} KB."

class Audiobook(Book):
    '''
    This class is responsible for creating instances of audiobooks. Therefore, the show_book_size method will display the book_size as the length in minutes of the audiobook. All other attributes and methods are inherited from the Book parent class.
    '''
    
    def __init__(self, book_id, **kwargs):
        super().__init__(book_id, **kwargs)
        self.title = kwargs["title"]
        self.length_minutes = kwargs["size"]
        
    def show_book_size(self):
        return f"The audiobook '{self.title}' has a length of {self.length_minutes} minutes."

class Factory:
    '''
    This class is responsible for creating new books. Thus, it can receive and validate data, generate unique book ID's, create instaces of the three child classes above, and add new books to the catalogue.
    '''
    
    def __init__(self, catalogue):
        self.catalogue = catalogue
        self.next_book_id = 1
    
    def _generate_unique_id(self):
        book_id = self.next_book_id
        self.next_book_id += 1
        return book_id
    
    def generate_book_from_data(self, row):     
        common_args = {
            "title": row["title"],
            "author": row["author"],
            "description": row["description"],
            "category": row["category"],
            "medium": row["medium"],
            "audience": row["audience"],
            "size": row["size"],
            "purchase_price": round(float(row["purchase_price"]), 2),
            "selling_price": round(float(row["selling_price"]), 2),
            "stock": int(row["stock"])
        }
        self.create_new_book(**common_args)
    
    def create_new_book(self, **kwargs):
        medium = kwargs["medium"].lower()
        book_id = self._generate_unique_id()
        if medium == "printed":
            self.catalogue.add_book(PrintedBook(book_id, **kwargs))
        elif medium == "audiobook":
            self.catalogue.add_book(Audiobook(book_id, **kwargs))
        elif medium == "e-book":
            self.catalogue.add_book(EBook(book_id, **kwargs))
        
    def _validate_book_data(self, **kwargs):
        for key, value in kwargs.items():
            kwargs[key] = str(value).strip()
        
        required_fields = ["title", "author", "description", "category", "medium", "audience", "size", "purchase_price", "selling_price", "stock"]
        for field in required_fields:
            if field not in kwargs or not kwargs[field]:
                return f"Missing or empty required field: {field}", None
        
        try:
            kwargs["title"] = str(kwargs["title"])
            kwargs["author"] = str(kwargs["author"])
            kwargs["description"] = str(kwargs["description"])
            kwargs["category"] = str(kwargs["category"]).capitalize()
            kwargs["medium"] = str(kwargs["medium"]).capitalize()
            kwargs["audience"] = str(kwargs["audience"]).capitalize()
            kwargs["size"] = int(kwargs["size"])
            kwargs["purchase_price"] = round(float(kwargs["purchase_price"]),)
            kwargs["selling_price"] = round(float(kwargs["selling_price"]),)
            kwargs["stock"] = int(kwargs["stock"])
        except ValueError as e:
            return f"Error converting data: {str(e)}", None
        
        if kwargs["category"] not in ["Fiction", "Non-fiction"]:
            return f"Invalid category value. Category must be 'fiction' or 'non-fiction'.", None
        
        if kwargs["medium"] not in ["Printed", "Audiobook", "E-book"]:
            return f"Invalid medium value. Medium must be 'printed', 'audiobook' or 'e-book'.", None
        
        if kwargs["audience"] not in ["Children", "Young adults", "Adults"]:
            return f"Invalid audience value. Audience must be 'children', 'young adults' or 'adults'.", None
        
        return None, kwargs
    
    def handle_new_book_input(self, **kwargs):
        validation_error, validated_data = self._validate_book_data(**kwargs)
        if validation_error:
            return validation_error
        self.create_new_book(**validated_data)

class Catalogue:
    '''
    This class is responsible for managing the bookstore catalogue/stock. Thus, it adds newly created books to the catalogue after they have been created in the Factory. The class is also responsible for deletion of a book, for all search functionality, and for generating stock lists.
    '''
    
    def __init__(self):
        self.books = []
    
    def add_book(self, new_book):
        for book in self.books:
            if book.title.lower() == new_book.title.lower() and book.author.lower() == new_book.author.lower() and book.medium.lower() == new_book.medium.lower():
                print(f"The book {new_book.title} by {new_book.author} already exists in the catalogue.")
                return
        self.books.append(new_book)
    
    def delete_book(self, book_id):
        try:
            book_id = int(book_id)
        except ValueError:
            print(f"Invalid book ID. Please provide an ID consisting of only numeric characters.")
        
        for book in self.books:
            if book.book_id == book_id:
                self.books.remove(book)
                return f"The book with the title '{book.title}' and the ID {book_id} was successfully removed."

        return f"No book with the provided ID {book_id} was found in the catalogue."
    
    def get_unique_categories(self):
        unique_categories = {book.category for book in self.books}
        return [{"id": index, "category": category} for index, category in enumerate(unique_categories, start=1)]
    
    def search_book(self, query_type, query_value):        
        validation_error, validated_query_type, validated_query_value = self._validate_query(query_type, query_value)
        if validation_error:
            return validation_error
        
        matching_books = []
        for book in self.books:
            attribute_value = str(getattr(book, validated_query_type)).lower()
            if attribute_value == validated_query_value:
                matching_books.append(str(book))
        
        if matching_books:
            return "\n".join(matching_books)
        else:
            return f"No books matching the query type {query_type} and the query value {query_value} found in the catalogue."

    def _validate_query(self, query_type, query_value):
        try:
            query_type = str(query_type).strip().lower()
        except ValueError:
            return f"Error converting query type to a string: {query_type}.", None
        
        try:
            query_value = str(query_value).strip().lower()
        except ValueError:
            return f"Error converting query value to a string: {query_value}", None
        
        if query_type == "book_id":
            try:
                int(query_value)
            except ValueError:
                return f"Invalid {query_type}: {query_value}. Please provide a valid ID consisting of only numerical characters.", None
        elif query_type not in ["title", "author", "category", "medium"]:
            return f"Invalid query type: {query_type}. Please provide one of the following query types: id, title, author, category, or medium.", None
        
        return None, query_type, query_value
    
    def generate_stock_lists(self, sorting_choice):
        sorted_books = []
        
        if sorting_choice == "alphabetical_author":
            self.books.sort(key=lambda book: book.author.split()[-1])
        elif sorting_choice == "alphabetical_title":
            self.books.sort(key=lambda book: book.title)
        elif sorting_choice == "category":
            self.books.sort(key=lambda book: book.category)
        elif sorting_choice == "medium":
            self.books.sort(key=lambda book: book.medium)
        elif sorting_choice == "ascending_stock":
            self.books.sort(key=lambda book: book.stock)
        elif sorting_choice == "descending_stock":
            self.books.sort(key=lambda book: book.stock, reverse=True)
        
        for book in self.books:
            sorted_books.append(str(book))
        
        return "\n".join(sorted_books)