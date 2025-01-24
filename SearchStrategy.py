class SearchStrategy:
    def search(self, books, query):
       pass


"""
Searches for books with a title matching the query.
Takes a list of book dictionaries and a title query as input.
Returns a list of books that have an exact match for the specified title.
"""
class SearchByTitle(SearchStrategy):
    def search(self, books, query):
        selected_books = []
        for row in books:
            if query.lower() == row['title'].lower():
                selected_books.append(row)
        return selected_books


"""
Searches for books with an author name matching the query.
Takes a list of book dictionaries and an author query as input.
Returns a list of books that have an exact match for the specified author name.
"""
class SearchByAuthor(SearchStrategy):
    def search(self, books, query):
        selected_books = []
        for row in books:
            if query.lower() == row['author'].lower():
                selected_books.append(row)
        return selected_books


"""
Searches for books with a publication year matching the query.
Takes a list of book dictionaries and a year query as input.
Returns a list of books that match the specified year, ignoring invalid year formats.
"""
class SearchByYear(SearchStrategy):
    def search(self, books, query):
        selected_books = []
        for row in books:
            try:
                book_year = int(row['year'])
                if book_year == query:
                    selected_books.append(row)
            except ValueError:
                continue
        return selected_books


"""
Searches for books with a genre matching the query (case-insensitive).
Takes a list of book dictionaries and a genre query as input.
Returns a list of books that match the specified genre.
"""
class SearchByGenre(SearchStrategy):
    def search(self, books, query):
        selected_books = []
        for row in books:
            if query.lower() == row['genre'].lower():
                selected_books.append(row)
        return selected_books