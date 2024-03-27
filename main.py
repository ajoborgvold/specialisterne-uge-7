
import csv
from classes import Catalogue, Factory

def display_menu():
    '''
    This function displays the main menu for interacting with the bookstore management system.
    '''
    
    print("Welcome to the bookstore management system!")
    print("1. Add a new book.")
    print("2. Search for a book.")
    print("3. Delete a book.")
    print("4. Get reports on the bookstore's stock.")
    print("5. Exit.")
    print()


def generate_books_from_csv(factory, filepath):
    '''
    This function fetches data from the local file `books_data.csv` and passes this data on to the `factory`, where new book objects are then created and added to the `catalogue`.
    The function is called from the add_new_book function, when the user selects the first option, 'Add books from a data file'. The purpose of this functionality is to allow the user to interact with the bookstore management system without having to manually add books to the system.
    '''
    
    with open(filepath) as file:
        reader = csv.DictReader(file)
        for row in reader:
            factory.generate_book_from_data(row)

def add_new_book(factory, catalogue):
    '''
    This function displays a menu for adding new books. It gives the user two options: add books from a local data file, or enter new data manually. When the latter is selected, the method handle_new_book_input in the `factory` is called. Here, there data is first validated and then a new book object is created and added to the `catalogue`.
    '''
    
    while True:
        print("Add new books to the book catalogue.")
        print("Options:")
        print("1. Add books from a data file.")
        print("2. Enter new data.")
        print("3. Exit and return to the main menu.")
        main_choice = input("Enter your choice (1-3): ").strip()
        
        if main_choice == "1":
            generate_books_from_csv(factory, "books_data.csv")
            print("25 books added.")
            submenu_choice = input("Enter p to print the books or e to exit and return to the main menu: ").strip().lower()
            
            if submenu_choice == "p":
                for book in catalogue.books:
                    print(book)
                print()
                continue
            elif submenu_choice == "e":
                break
            else:
                print(f"Invalid selection: {submenu_choice}. Returning to main menu.")
                break
            
        elif main_choice == "2":            
            print("\nEnter new data to add a book to the catalogue.")
            print()
            title = input("Enter the book's title:\n")
            author = input("Enter the author(s):\n")
            description = input("Enter a description of the book:\n")
            category = input("Select a category (Fiction or Non-fiction):\n")
            medium = input("Select a medium (Printed, Audiobook, or E-book):\n")
            audience = input("Select a target audience (Children, Young adults, or Adults):\n")
            size = input("Enter the size, i.e. number of pages (printed books), length in minutes (audiobooks) or byte size in KB (e-books):\n")
            purchase_price = input("Enter the purchase price:\n")
            selling_price = input("Enter the selling price:\n")
            stock = input("Enter the current stock, i.e. how many copies you're adding:\n")
            print()
            
            args = {
                "title": title,
                "author": author,
                "description": description,
                "category": category,
                "medium": medium,
                "audience": audience,
                "size": size,
                "purchase_price": purchase_price,
                "selling_price": selling_price,
                "stock": stock
            }
            
            validation_result = factory.handle_new_book_input(**args)
            if validation_result:
                print(validation_result)
                print("Returning to main menu.")
                break
            else:
                print("Book added successfully!")
                submenu_choice = input("Enter p to print the book or e to exit and return to the main menu: ").strip().lower()
                if submenu_choice == "p":
                    print(catalogue.books[-1])
                    print()
                    continue
                elif submenu_choice == "e":
                    print("Returning to main menu.")
                    print()
                    break
                else:
                    print(f"Invalid selection: {submenu_choice}. Returning to main menu.")
                    break
            
        elif main_choice == "3":
            print(f"Returning to menu.")
            break
        else:
            print(f"Invalid selection. Please try again.")

def search_catalogue(catalogue):
    '''
    This menu enables searches in the catalogue. Books can be found based on their ID, title, author, category and medium. The user selects a query type and enters a query value, which is then passed to the search_book method in the `catalogue`. Here, the queries are first validated, and then search result is returned.
    '''
    
    query_options = {
        "1": "book_id",
        "2": "title",
        "3": "author",
        "4": "category",
        "5": "medium"
    }
    
    while True:
        print("Search in the bookstore catalogue.")
        print("Options:")
        print("1. Search by book ID.")
        print("2. Search by book title.")
        print("3. Search by author")
        print("4. Search by category (fiction or non-fiction).")
        print("5. Search by medium (printed book, audiobook, or e-book).")
        print("6. Exit and return to the main menu.")
        print()
        
        choice = input("Enter your choice (1-6): ").strip()
        print()
        
        if choice == "6":
            print("Returning to main menu.")
            print()
            break
        
        if choice not in query_options:
            print("Invalid choice. Please enter a number from 1 to 6.")
            print()
        
        query_type = query_options[choice]
        query_value = input(f"Enter the {query_type} that you want to search for:\n").strip()
        print()
        
        search_result = catalogue.search_book(query_type, query_value)
        print("Search result:")
        print(search_result)

def delete_book(catalogue):
    '''
    This menu allows you to delete a book from the catalogue by entering the ID of the book you want to delete.
    '''
    
    print("Delete a book from the catalogue.")
    book_id = input("Enter the ID of the book you want to delete: ").strip()
    print()
    
    deleted_book = catalogue.delete_book(book_id)
    print(deleted_book)
    

def get_reports(catalogue):
    '''
    This menu allows you to generate sorted stock lists. You are asked to choose how you want the lists sorted. Your choice is then passed to the generate_stock_lists method in the `catalogue` which returns a sorted list of stock items.
    '''
    
    sorting_options = {
        "1": "alphabetical_author",
        "2": "alphabetical_title",
        "3": "category",
        "4": "medium",
        "5": "ascending_stock",
        "6": "descending_stock"
    }
    
    while True:
        print("Generate reports on the bookstore's stock.")
        print()
        print("Choose how you want the stock items sorted:")
        print("1. Alphabetically by author's last name.")
        print("2. Alphabetical by title.")
        print("3. Grouped by category.")
        print("4. Grouped by medium.")
        print("5. Stock, ascending order.")
        print("6. Stock, descending order.")
        print("7. Exit and return to main menu.")
        print()
        
        choice = input("Enter your choice (1-7): ")
        print()
        
        if choice == "7":
            print("Returning to main menu.")
            break
        
        if choice not in sorting_options:
            print("Invalid choice. Please enter a number from 1 to 7.")
            print()
            
        sorting_choice = sorting_options[choice]
        
        stock = catalogue.generate_stock_lists(sorting_choice)
        print(stock)
        print()

def main():
    '''
    This function handles the functionality of the main menu. The menu runs in a loop untill the user chooses to exit.
    '''
    
    catalogue = Catalogue()
    factory = Factory(catalogue)
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ")
        print()
        
        if choice == "1":
            add_new_book(factory, catalogue)
        elif choice == "2":
            search_catalogue(catalogue)
        elif choice == "3":
            delete_book(catalogue)
        elif choice == "4":
            get_reports(catalogue)
        elif choice == "5":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 5.")
        print()


if __name__ == "__main__":
    main()