class Book:
    def __init__(self, title, author, year, genre, copies):
        self.__title = title  
        self.__author = author  
        self.__is_loaned = "No"
        self.__copies = int(copies)  
        self.__genre = genre  
        self.__year = year  
        self.__available_Copies = copies
        self.__waiting_list = ""
        self.__popularity = 0


    def to_dict(self):
        return {
            "title": self.__title,
            "author": self.__author,
            "is_loaned": self.__is_loaned,
            "copies": self.__copies,
            "genre": self.__genre,
            "year": self.__year,
            "available_copies": self.__copies,
            "popularity": self.__popularity,
            "waiting_list": self.__waiting_list
        }  

