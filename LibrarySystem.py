import hashlib
import logging

import CSV
import Obserever
from Book import Book
from CsvIterator import CsvIterator
from SearchStrategy import SearchByTitle, SearchByAuthor, SearchByYear, SearchByGenre
logging.basicConfig(filename='library.log',level=logging.DEBUG,format='%(message)s')
def log_note (message): logging.log(logging.DEBUG, message)


'''
בס"ד 

 This class manages the library system.
 It contains methods for adding, removing, and searching books.
 It also manages the users and their credentials.
'''
class LibrarySystem:
    def __init__(self):
        self.books = CSV.read_csv('books.csv')  
        self.users = CSV.read_csv('users.csv')  
        self.loaned_books = CSV.read_csv('loaned_books.csv')
        self.popular_books = CSV.read_csv('popular_books.csv')
        self.available_books = CSV.read_csv('available_books.csv')
        self.update_available_books()
        self.update_loaned_books()
        self.update_popular_books()

    '''
    Register a new user.
    '''
    def register_user(self, username, password):
        if any(user['username'] == username for user in self.users):
            log_note("registered fail")
            raise ValueError("User already exists.")  
        hashed_password = self.hash_password(password)  
        self.users.append({"username": username, "password": hashed_password})  
        CSV.write_csv('users.csv', self.users, fieldnames=['username', 'password'])  
        log_note("registered successfully")

    '''
    Authenticate a user.
    '''
    def authenticate_user(self, username, password):
        hashed_password = self.hash_password(password)  
        return any(user['username'] == username and user['password'] == hashed_password for user in self.users)

    '''
    Hash a password using SHA-256.
    '''
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    """
    Adds a new book or updates copies if the book already exists. Validates all inputs, ensuring non-empty fields and
    integer values for year and copies (copies > 0). Logs success or error messages and updates the library data.
    """

    def add_book(self, title, author, year, category, copies, win):
        try:
            if not title.strip() or not author.strip() or not year.strip() or not category.strip() or not copies.strip():
                Obserever.notify("Error", "All fields are required!")
                log_note("book added fail")
                return  
            try:
                year = int(year)
                copies = int(copies)
            except ValueError:
                Obserever.notify("Error", "Year and Copies must be valid integers!")
                log_note("book added fail")
                return  
            if copies <= 0:
                Obserever.notify("Error", 'Copies must be a positive integer!')
                log_note("book added fail")
                return
            for book in self.books:
                if book['title'].lower() == title.lower():  
                    book['copies'] = str(int(book['copies']) + int(copies))  
                    book['available_copies'] = str(int(book['available_copies']) + int(copies))  
                    CSV.write_csv('books.csv', self.books,
                                  fieldnames=["title", "author", "is_loaned", "copies", "genre", "year",
                                              "available_copies", "popularity", "waiting_list"])
                    Obserever.notify("Success", f"Book '{title}' updated successfully!")  
                    win.destroy()  
                    self.update_available_books()
                    self.update_loaned_books()
                    return  
            else:
                book = Book(title, author, year, category, copies)  
                self.books.append(book.to_dict())  
                CSV.write_csv('books.csv',self.books, fieldnames=[ "title", "author", "is_loaned","copies","genre","year",
                 "available_copies", "popularity", "waiting_list"])
                Obserever.notify("Success", "Book added successfully!")
                log_note("book added successfully")
                self.update_available_books()

            win.destroy()  
        except Exception as e:
            Obserever.notify("Error", str(e))  
            log_note("book added fail")

    """
    Removes a book by title if it exists in the library. Logs success or failure, updates CSV files, and refreshes 
    available, loaned, and popular books data.
    """

    def remove_book(self, title):
        book_found = any(book['title'].strip().lower() == title.strip().lower() for book in self.books)
        if not book_found:
            log_note('book removed fail')
            Obserever.notify("Error", "Book not found.")
            return  
        self.books = [book for book in self.books if book['title'].strip().lower() != title.strip().lower()]
        if self.books:
            CSV.write_csv('books.csv', self.books, fieldnames=self.books[0].keys())
        else:
            CSV.write_csv('books.csv', [],
                          fieldnames=['title', 'author', 'is_loaned', 'copies', 'genre', 'year', 'available_copies',
                                      'popularity', 'waiting_list'])
        self.update_available_books()
        self.update_loaned_books()
        self.update_popular_books()
        log_note('book removed successfully')
        Obserever.notify("Success", "Book removed successfully!")

    """
    Handles the removal of a book by calling the `remove_book` function.
    Validates the book's existence, removes it from the library, and updates
    the library system's relevant files. Finally, closes the UI window to complete the action.
    """

    def handle_remove_book(self, title, win):
        try:
            self.remove_book(title)  
            win.destroy()  

        except Exception as e:
            Obserever.notify("Error", str(e))


    """
    Searches for books in the library using various criteria such as title, author, year, or genre.
    Uses specific search strategies depending on the search type.
    Logs whether the search succeeded or failed, closes the search window, and returns the search results.
    """

    def handle_searched_books(self, search_type_num, user_query, win):
        relevant_books = []
        user_query = str(user_query).strip()
        books_file = CsvIterator("books.csv")

        if search_type_num == 0:
            relevant_books = SearchByTitle().search(books_file, user_query)
            if len(relevant_books) == 0:
                log_note(f'Search book "{user_query}" by name completed fail')
            else:
                log_note(f'Search book "{user_query}" by name completed successfully')

        if search_type_num == 1:
            relevant_books = SearchByAuthor().search(books_file, user_query)
            if len(relevant_books) == 0:
                log_note(f'Search book by author name completed fail')
            else:
                for row in relevant_books:
                    log_note(f'Search book "{row["title"]}" by author name completed successfully')

        if search_type_num == 2:
            try:
                query_year = int(user_query)
                relevant_books=SearchByYear().search(books_file, query_year)
            except ValueError:
                Obserever.notify('Error',f'Invalid year format for book ')

        if search_type_num == 3:
           relevant_books = SearchByGenre().search(books_file, user_query)

        win.destroy()
        return relevant_books



    """
    Authenticates a user by validating the username and hashed password against the stored users.
    Logs the login attempt's success or failure, notifies the user of the outcome, and returns a boolean result.
    """
    def handle_login(self, username, password):
        try:
            if self.authenticate_user(username, password):  
                Obserever.notify("Success", "Logged in successfully!")  
                log_note("logged in successfully")

                return True
            else:
                Obserever.notify("Error", "Invalid credentials.")  
                log_note("logged in fail")

        except Exception as e:
            Obserever.notify("Error", str(e))



    """
    Registers a new user by verifying that the username does not already exist in the system.
    If valid, it saves the username and hashed password to the users' dataset.
    Logs the registration status, notifies the user, and closes the registration window on success.
    """

    def handle_register(self, username, password, win):
        try:
            self.register_user(username, password)  
            Obserever.notify("Success", "Registered successfully!")  
            win.destroy()  
        except Exception as e:
            Obserever.notify("Error", str(e))




    """
    Processes a book loan request. If copies are available, it decreases the
    available count and increases the book's popularity. Updates relevant
    files and returns statuses like "success" or "no_copies" based on the action outcome.
    """
    def loan_book(self, title):
        
        try:
            for book in self.books:
                if book['title'].lower() == title.lower():
                    if int(book['available_copies']) > 0:
                        book['available_copies'] = str(int(book['available_copies']) - 1)
                        book['popularity'] = str(int(book['popularity']) + 1)
                        if book['available_copies'] == '0':
                            book['is_loaned'] = 'Yes'
                        CSV.write_csv(
                            'books.csv',self.books,fieldnames=["title", "author", "is_loaned", "copies",
                                    "genre","year", "available_copies", "popularity", "waiting_list"])
                        self.update_popular_books()
                        self.update_available_books()
                        self.update_loaned_books()
                        return "success"
                    else:
                        return "no_copies"
            return "error"  
        except Exception as e:
            return str(e)



    """
    Adds a user to the waiting list of a specific book. Formats and appends
    the user's details (full name, email, phone) to the waiting list.
    Updates the book's popularity, saves the updated data to the library files, and handles potential errors.
    """

    def add_to_waiting_list(self, title, full_name, email, phone):
        
        try:
            for book in self.books:
                if book["title"].lower() == title.lower():
                    waiting_list_str = str(book["waiting_list"]).strip()  
                    waiting_list = waiting_list_str.split(",") if waiting_list_str else []
                    waiting_list = [entry for entry in waiting_list if entry.lower() != "nan"]
                    new_entry = f"{full_name}|{email}|{phone}"
                    waiting_list.append(new_entry)
                    book["waiting_list"] = ",".join(waiting_list)
                    book['popularity'] = str(int(book['popularity']) + 1)
                    CSV.write_csv('books.csv', self.books, fieldnames=["title", "author", "is_loaned",
                    "copies", "genre", "year", "available_copies","popularity", "waiting_list"])
                    self.update_popular_books()
                    self.update_available_books()
                    self.update_loaned_books()
                    return  

            raise ValueError("Book not found in library.")
        except Exception as e:
            raise e



    """
    Handles the return of a book. Updates its availability count and notifies the next
    person in the waiting list if applicable. Adjusts the waiting list and availability data,
    updates library files, and closes the UI window upon completion.
    """
    def handle_return_book(self, tree, win):
        selected_item = tree.selection()
        if not selected_item:
            Obserever.notify("Error", "Please select a book first.")
            return
        selected_book = tree.item(selected_item[0])["values"]
        for book in self.books:
            if book['title'].lower() == selected_book[0].lower():
                waiting_list_str = str(book["waiting_list"]).strip()  
                waiting_list = waiting_list_str.split(",") if waiting_list_str else []
                if waiting_list:
                    Obserever.notify("Notify", f'The book "{selected_book[0]}" has been returned\n '
                     f'The system already loaned the book to\n {waiting_list[0]}\n Use those details to contact the user')
                    waiting_list.pop(0)  

                    book["waiting_list"] = ",".join(waiting_list)  
                else:
                    book['available_copies'] = str(int(book['available_copies']) + 1)
                    log_note('book returned successfully')
                    if book['is_loaned'] == 'Yes':
                        book['is_loaned'] = 'No'

                CSV.write_csv('books.csv', self.books, fieldnames=["title", "author", "is_loaned", "copies",
                "genre", "year", "available_copies", "popularity","waiting_list"])
                self.update_available_books()
                self.update_loaned_books()
                self.update_popular_books()
                win.destroy()
                return

        Obserever.notify("Error", "Book not found.")

    """
    Updates the list of available books by identifying books with more than
    zero copies. Saves the filtered data to a dedicated file for available books,
    ensuring the system reflects current availability.
    """

    def update_available_books(self):
        available_books = []
        books_iterator = CsvIterator("books.csv")
        for book in books_iterator:
            if int(book['available_copies']) > 0:
                available_books.append(book)
        CSV.write_csv("available_books.csv", available_books,
                      fieldnames=["title", "author", "is_loaned", "copies", "genre", "year", "available_copies",
                                  "popularity", "waiting_list"])

    """
    Creates and updates a list of loaned books by checking which books
    have fewer available copies than their total. Adjusts the 'is_loaned' field
    accordingly and writes this updated list to a loaned books file.
    """

    def update_loaned_books(self):
        loaned_books = []
        books_iterator = CsvIterator("books.csv")
        for book in books_iterator:
            if int(book['available_copies']) < int(book['copies']):
                if int(book['available_copies']) == 0:
                    book['is_loaned'] = 'Yes'
                loaned_books.append(book)
            else: book['is_loaned'] = 'No'
        CSV.write_csv("loaned_books.csv", loaned_books,fieldnames=["title", "author",
                "is_loaned", "copies", "genre", "year", "available_copies","popularity", "waiting_list"])

    """
    Generates a list of the top 10 most popular books by sorting the library data
    based on the popularity metric. Saves the sorted list to a dedicated
    file for popular books, keeping it up-to-date for user queries.
    """

    def update_popular_books(self):
        import csv
        try:
            with open("books.csv", mode="r", encoding="utf-8") as books_file:
                reader = csv.DictReader(books_file)
                books = list(reader)
            for book in books:
                book["popularity"] = int(book.get("popularity", 0))  

            sorted_books = sorted(books, key=lambda book: book["popularity"], reverse=True)[:10]
            CSV.write_csv("popular_books.csv",sorted_books, fieldnames=["title", "author","is_loaned","copies",
                                    "genre", "year","available_copies", "popularity","waiting_list"])
        except FileNotFoundError:
            print("Error: books.csv file not found.")
        except Exception as e:
            print(f"An error occurred: {e}")




    @staticmethod
    def get_all_genres():
        genres = []
        genres_iterator = CsvIterator("books.csv")
        for book in genres_iterator:
            if book['genre'] not in genres:
                genres.append(book['genre'])
        return genres