class Book:  # a Book Class with it's features
    def __init__(self, title, publisher, isbn10,isbn13,copies, **Other):  #Book Arguments and features
        self.title = title
        self.publisher = publisher
        self.isbn10 = isbn10
        self.isbn13 = isbn13
        self.copies = copies  #number of copies
        self.archived = False  #set to false
        self.extra_info = Other

    def __str__(self):
        book_information = f"Title : {self.title}\nPublisher : {self.publisher}\nISBN-10 : {self.isbn10}\nISBN-13 : {self.isbn13}"
        for key, value in self.extra_info.items():  #loop to show the extra information of books
            book_information += f"\n{key} : {value}"
        return book_information