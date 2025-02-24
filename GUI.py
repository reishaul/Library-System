#Implements and logic by Ron Avraham - ronavraham1999@gmail.com, Rei Shaul - reishaul1@gmail.com
import tkinter as tk
import Obserever
from tkinter import ttk
import LibrarySystem
from CsvIterator import CsvIterator
from LibrarySystem import LibrarySystem
from LibrarySystem import log_note


class LibraryApp:
    def __init__(self, root):
        self.library = LibrarySystem()
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("300x300")
        self.create_main_screen()

    '''
    Create main screen 
    '''
    def create_main_screen(self):
        tk.Label(self.root, text="Welcome to the Library", font=("Helvetica", 16)).pack(pady=20)
        tk. Button(self.root, text="Login", command=self.login_screen).pack(pady=40)
        tk.Button(self.root, text="Register", command=self.register_screen).pack(pady=10)

    '''
    Create login screen
    '''
    def login_screen(self):
        login_win = tk.Toplevel(self.root)
        login_win.geometry("250x200")
        login_win.title("Login")

        tk.Label(login_win, text="Username:").pack(pady=5)
        username = tk.StringVar()
        tk.Entry(login_win, textvariable=username).pack(pady=5)

        tk.Label(login_win, text="Password:").pack(pady=5)
        password = tk.StringVar()
        tk.Entry(login_win, textvariable=password, show="*").pack(pady=5)

        (tk.Button(login_win, text="Login", command=lambda: self.open_dashboard(username.get(), password.get(), login_win)).pack(pady=10))


    def open_dashboard(self, username, password, win):
        if self.library.handle_login(username, password):
            self.root.withdraw()
            win.destroy()
            self.create_dashboard()


    def register_screen(self):
        register_win = tk.Toplevel(self.root)
        register_win.title("Register")
        register_win.geometry("250x200")

        tk.Label(register_win, text="Username:").pack(pady=5)
        username = tk.StringVar()
        tk.Entry(register_win, textvariable=username).pack(pady=5)

        tk.Label(register_win, text="Password:").pack(pady=5)
        password = tk.StringVar()
        tk.Entry(register_win, textvariable=password, show="*").pack(pady=5)

        tk.Button(register_win, text="Register", command=lambda: self.library.handle_register(username.get(), password.get(), register_win)).pack(pady=10)



    def create_dashboard(self):
        dashboard = tk.Toplevel(self.root)
        dashboard.title("Dashboard")
        dashboard.geometry("600x500")

        tk.Label(dashboard, text="Library Dashboard", font=("Helvetica", 16)).pack(pady=20)

        tk.Button(dashboard, text="Add Book ➕",font=("Helvetica", 14), command=self.add_book_screen).pack(pady=10)

        tk.Button(dashboard, text="Remove Book ➖",font=("Helvetica", 14), command=self.remove_book_screen).pack(pady=10)

        tk.Button(dashboard, text="Search Book 🔎",font=("Helvetica", 14), command=self.search_books_screen).pack(pady=10)

        tk.Button(dashboard, text="View Books 👓",font=("Helvetica", 14), command=self.choose_view_books_screen).pack(pady=10)

        tk.Button(dashboard, text="Lend Book ➡️",font=("Helvetica", 14), command=self.loan_book_screen).pack(pady=10)

        tk.Button(dashboard, text="Return Book ⬅️",font=("Helvetica", 14), command=self.return_book_screen).pack(pady=15)
        tk.Button(dashboard, text="Logout",font=("Helvetica", 14),fg="red", command=self.logout).pack(pady=10)

    def add_book_screen(self):
        add_win = tk.Toplevel(self.root)
        add_win.title("Add Book")
        add_win.geometry("250x400")
        tk.Label(add_win, text="Title:").pack(pady=5)
        title = tk.StringVar()
        tk.Entry(add_win, textvariable=title).pack(pady=5)  

        tk.Label(add_win, text="Author:").pack(pady=5)  
        author = tk.StringVar()
        tk.Entry(add_win, textvariable=author).pack(pady=5)  

        tk.Label(add_win, text="Year:").pack(pady=5)  
        year = tk.StringVar()
        tk.Entry(add_win, textvariable=year).pack(pady=5)  

        tk.Label(add_win, text="Genre:").pack(pady=5)  
        genre = tk.StringVar()
        tk.Entry(add_win, textvariable=genre).pack(pady=5)  

        tk.Label(add_win, text="Copies:").pack(pady=5)  
        copies = tk.StringVar()
        tk.Entry(add_win, textvariable=copies).pack(pady=5)  


        tk.Button(add_win, text="Add Book", command=lambda: self.library.add_book(title.get(), author.get(), year.get(), genre.get(), copies.get(), add_win)).pack(pady=10)  



    def remove_book_screen(self):
        remove_win = tk.Toplevel(self.root)  
        remove_win.title("Remove Book")
        remove_win.geometry("250x150")

        tk.Label(remove_win, text="Enter the title of the book:").pack(pady=5)
        title = tk.StringVar()
        tk.Entry(remove_win, textvariable=title).pack(pady=5)  

        tk.Button(remove_win, text="Remove Book", command=lambda: self.library.handle_remove_book(title.get(), remove_win)).pack(pady=10)  


    def search_books_screen(self):
        search_win = tk.Toplevel(self.root)
        search_win.geometry("400x500")
        search_win.title("Search Books")
        tk.Label(search_win, text="Search books by:",font=("Helvetica", 13)).pack(pady=30)  

        tk.Label(search_win, text="Title:").pack(pady=5)  
        title = tk.StringVar()
        tk.Entry(search_win, textvariable=title).pack(pady=5)  
        tk.Button(search_win, text="Search", command=lambda:
        self.found_books_screen(
            self.library.handle_searched_books(0,title.get(), search_win))).pack(pady=10)

        tk.Label(search_win, text="Author:").pack(pady=5)  
        author = tk.StringVar()
        tk.Entry(search_win, textvariable=author).pack(pady=5)  
        tk.Button(search_win, text="Search", command=lambda:
        self.found_books_screen(
            self.library.handle_searched_books(1,author.get(), search_win))).pack( pady=10)

        tk.Label(search_win, text="Year:").pack(pady=5)  
        year = tk.StringVar()
        tk.Entry(search_win, textvariable=year).pack(pady=5)  
        tk.Button(search_win, text="Search", command=lambda:
        self.found_books_screen(
            self.library.handle_searched_books(2,year.get(), search_win))).pack(pady=10)

        tk.Label(search_win, text="Genre:").pack(pady=5)  
        genre = tk.StringVar()
        tk.Entry(search_win, textvariable=genre).pack(pady=5)  
        tk.Button(search_win, text="Search", command=lambda: self.found_books_screen
        (self.library.handle_searched_books(3,genre.get(), search_win))).pack(pady=10)

    def found_books_screen(self, relevant_books):
        found_books_win = tk.Toplevel(self.root)
        found_books_win.geometry("1500x500")
        found_books_win.title("Found Books")
        columns = ("title", "author", "year", "genre", "is loaned", "copies", "available copies", "popularity","waiting list")
        tree = ttk.Treeview(found_books_win, columns=columns, show="headings")
        tree.pack(fill=tk.BOTH, expand=True)
        for column in columns:
            tree.heading(column, text=column.title())  
            tree.column(column, width=60 if column in ["year", "copies", "is loaned", "available copies",
                                                       "popularity"] else 100, anchor=tk.W)
        tree.heading("title", text="Title")
        tree.heading("author", text="Author")
        tree.heading("year", text="Year")
        tree.heading("genre", text="Genre")
        tree.heading("is loaned", text="Is Loaned")
        tree.heading("copies", text="Copies")
        tree.heading("available copies", text="Available Copies")
        tree.heading("popularity", text="Popularity")
        tree.heading("waiting list", text="Waiting List")
        for book in relevant_books:
            tree.insert("", tk.END, values=(book["title"], book["author"], book["year"], book["genre"],
                                book["is_loaned"], book["copies"],book["available_copies"], book["popularity"],book["waiting_list"]))
        tk.Button(found_books_win, text="Close", command=found_books_win.destroy).pack(pady=10)

    def choose_view_books_screen(self):
        choose_view_win = tk.Toplevel(self.root)
        choose_view_win.geometry("400x500")
        choose_view_win.title("View Books")
        tk.Label(choose_view_win, text="Which books would you like to view?").pack(pady=5)

        tk.Button(choose_view_win,text="All books",command=lambda:self.view_books_screen(0,'books.csv')).pack(pady=10)
        tk.Button(choose_view_win,text="Available books",command=lambda:self.view_books_screen(1,'available_books.csv')).pack(pady=10)
        tk.Button(choose_view_win,text="Loaned books",command=lambda:self.view_books_screen(2,'loaned_books.csv')).pack(pady=10)
        tk.Button(choose_view_win,text="Popular books",command=lambda:self.view_books_screen(3,'popular_books.csv')).pack(pady=10)
        tk.Label(choose_view_win, text="You can also choose by genre:").pack(pady=15)

        options = self.library.get_all_genres()
        selected_option = tk.StringVar()
        selected_option.set(options[0])  
        dropdown = tk.OptionMenu(choose_view_win, selected_option, *options)
        dropdown.pack(pady=5)
        tk.Button(choose_view_win,text="View",command=lambda: self.by_chosen_genre_view_books_screen(selected_option.get())).pack(pady=5)

    def by_chosen_genre_view_books_screen(self, choose):
        chosen_view_win = tk.Toplevel(self.root)
        chosen_view_win.geometry("1500x500")
        chosen_view_win.title(choose)
        relevant_books = CsvIterator("books.csv")
        columns = ("title", "author", "year", "genre", "is loaned", "copies", "available copies", "popularity","waiting list")
        tree = ttk.Treeview(chosen_view_win, columns=columns, show="headings")
        tree.pack(fill=tk.BOTH, expand=True)
        for column in columns:
            tree.heading(column, text=column.title())  
            tree.column(column, width=40 if column in ["year", "copies", "is loaned", "available copies",
                                                       "popularity"] else 100, anchor=tk.W)
        tree.heading("title", text="Title")
        tree.heading("author", text="Author")
        tree.heading("year", text="Year")
        tree.heading("genre", text="Genre")
        tree.heading("is loaned", text="Is Loaned")
        tree.heading("copies", text="Copies")
        tree.heading("available copies", text="Available Copies")
        tree.heading("popularity", text="Popularity")
        tree.heading("waiting list", text="Waiting List")
        for book in relevant_books:
            if book['genre']==choose:
                tree.insert("", tk.END, values=(book["title"], book["author"], book["year"], book["genre"],
                                book["is_loaned"], book["copies"],book["available_copies"], book["popularity"],book["waiting_list"]))
        log_note(f'Displayed book by category successfully')
        tk.Button(chosen_view_win, text="Close", command=chosen_view_win.destroy).pack(pady=10)


    def view_books_screen (self,num_choose,choose):
        view_win = tk.Toplevel(self.root)
        view_win.geometry("1500x500")
        view_win.title(choose)
        relevant_books = CsvIterator(choose)

        columns = ("title", "author", "year", "genre", "is loaned", "copies", "available copies", "popularity","waiting list")
        tree = ttk.Treeview(view_win, columns=columns, show="headings")
        tree.pack(fill=tk.BOTH, expand=True)
        for column in columns:
            tree.heading(column, text=column.title())  
            tree.column(column, width=60 if column in ["year", "copies", "is loaned","available copies","popularity"] else 100, anchor=tk.W)
        tree.heading("title", text="Title")
        tree.heading("author", text="Author")
        tree.heading("year", text="Year")
        tree.heading("genre", text="Genre")
        tree.heading("is loaned", text="Is Loaned")
        tree.heading("copies", text="Copies")
        tree.heading("available copies", text="Available Copies")
        tree.heading("popularity", text="Popularity")
        tree.heading("waiting list", text="Waiting List")
        for book in relevant_books:
            tree.insert("", tk.END, values=(book["title"], book["author"], book["year"], book["genre"],
                                book["is_loaned"], book["copies"],book["available_copies"], book["popularity"],book["waiting_list"]))
        if num_choose==0:
            log_note(f'Displayed all books successfully')
        if num_choose==1:
            log_note(f'Displayed available books successfully')
        if num_choose==2:
            log_note(f'Displayed borrowed books successfully')
        if num_choose==3:
            log_note(f'Displayed popular books successfully')
        tk.Button(view_win, text="Close", command=view_win.destroy).pack(pady=10)

    def loan_book_screen(self):

        loan_win = tk.Toplevel(self.root)
        loan_win.title("Loan Book")
        loan_win.geometry("1500x500")

        columns = ("title", "author", "year", "genre", "is loaned", "copies", "available copies", "popularity","waiting list")
        tree = ttk.Treeview(loan_win, columns=columns, show="headings")
        tree.pack(fill=tk.BOTH, expand=True)

        for column in columns:
            tree.heading(column, text=column.title())
            tree.column(column, width=60 if column in ["year", "copies", "is loaned", "available copies",
                                                       "popularity"] else 100, anchor=tk.W)
        tree.heading("title", text="Title")
        tree.heading("author", text="Author")
        tree.heading("year", text="Year")
        tree.heading("genre", text="Genre")
        tree.heading("is loaned", text="Is Loaned")
        tree.heading("copies", text="Copies")
        tree.heading("available copies", text="Available Copies")
        tree.heading("popularity", text="Popularity")
        tree.heading("waiting list", text="Waiting List")
        books_iterator = CsvIterator("books.csv")
        for book in books_iterator:
            tree.insert("",tk.END,values=(book["title"], book["author"], book["year"], book["genre"],
                                book["is_loaned"], book["copies"],book["available_copies"], book["popularity"],book["waiting_list"]))
        tk.Button(loan_win,text="Loan book",command=lambda: self.loan_selected_book(tree, loan_win)).pack(pady=10)

    def loan_selected_book(self, tree, loan_win):
        selected_item = tree.selection()
        if not selected_item:
            Obserever.notify("Error", "Please select a book first.")
            return
        book_data = tree.item(selected_item[0])["values"]
        book_title = book_data[0]
        result = self.library.loan_book(book_title)

        if result == "success":
            Obserever.notify("Success", "Book loaned successfully!")
            loan_win.destroy()

        elif result == "no_copies":
            self.open_waiting_list_form(book_title,loan_win)

        else:
            Obserever.notify("Error", "An error occurred while loaning the book.")

    def open_waiting_list_form(self, book_title,win):
        wait_win = tk.Toplevel(self.root)
        wait_win.title("Waiting List")
        wait_win.geometry("400x300")
        tk.Label(wait_win, text="This book isn't available,\n But you can join it's waiting list down below:",font=("Helvetica", 11)).pack(pady=10)


        tk.Label(wait_win, text="Full Name:").pack(pady=5)
        full_name_var = tk.StringVar()
        tk.Entry(wait_win, textvariable=full_name_var).pack(pady=5)

        tk.Label(wait_win, text="Email:").pack(pady=5)
        email_var = tk.StringVar()
        tk.Entry(wait_win, textvariable=email_var).pack(pady=5)

        tk.Label(wait_win, text="Phone:").pack(pady=5)
        phone_var = tk.StringVar()
        tk.Entry(wait_win, textvariable=phone_var).pack(pady=5)
        submit_btn = tk.Button(wait_win,text="Add to waiting list",command=lambda: self.submit_waiting_list(
                book_title, full_name_var.get(),email_var.get(), phone_var.get(),wait_win,win))
        submit_btn.pack(pady=10)

    def submit_waiting_list(self, book_title, full_name, email, phone, wait_win,win):

        try:
            self.library.add_to_waiting_list(book_title, full_name, email, phone)
            Obserever.notify("Success", f"{full_name} have been added to the waiting list.")
            wait_win.destroy()
            win.destroy()
        except Exception as e:
            Obserever.notify("Error", str(e))

    def return_book_screen(self):

        return_book_win = tk.Toplevel(self.root)
        return_book_win.title("Return Book")
        return_book_win.geometry("1500x500")

        columns = ("title", "author", "year", "genre", "is loaned", "copies", "available copies", "popularity","waiting list")
        tree = ttk.Treeview(return_book_win, columns=columns, show="headings")
        tree.pack(fill=tk.BOTH, expand=True)

        for column in columns:
            tree.heading(column, text=column.title())  
            tree.column(column, width=60 if column in ["year", "copies", "is loaned", "available copies",
                                                       "popularity"] else 100, anchor=tk.W)
        tree.heading("title", text="Title")
        tree.heading("author", text="Author")
        tree.heading("year", text="Year")
        tree.heading("genre", text="Genre")
        tree.heading("is loaned", text="Is Loaned")
        tree.heading("copies", text="Copies")
        tree.heading("available copies", text="Available Copies")
        tree.heading("popularity", text="Popularity")
        tree.heading("waiting list", text="Waiting List")
        books_iterator = CsvIterator("loaned_books.csv")
        for book in books_iterator:
            tree.insert("",tk.END,values=(book["title"], book["author"], book["year"], book["genre"],
             book["is_loaned"], book["copies"],book["available_copies"], book["popularity"],book["waiting_list"]))
        tk.Button(return_book_win, text="Return book", command=lambda: self.library.handle_return_book(tree, return_book_win)).pack(pady=10)

    def logout(self):
        for window in self.root.winfo_children():
            if isinstance(window, tk.Toplevel):
                window.destroy()  
                log_note('logout successfully')
                self.root.deiconify()

if __name__ == "__main__":
    root = tk.Tk()  
    app = LibraryApp(root)  
    root.mainloop()  

