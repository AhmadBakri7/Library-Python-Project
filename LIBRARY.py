from BOOK import Book  #importing Class Book


class Library:  #a Library Class to perform actions on Books
    def __init__(self):
        self.books = []  #Books List

    def add(self, file_path):  #Adding a book to the library
        try:
            with open(file_path, 'r') as file:  #passing the file name
                book_data = {}  #Dictionary for books Inforamtions
                for l in file:  #loop for each line in the file
                    l = l.strip()
                    if l:  #checks if the line is empty or not
                        key, value = l.split(':', 1)
                        book_data[key.strip()] = value.strip() #splitting the data to store it into keys and values
                        print(key,":",value)
                        if 'Title' in book_data and 'Publisher' in book_data and 'ISBN-10' in book_data  and 'ISBN-13' in book_data:
                            # Assiging each value in the dictionary to it's similar in the book
                            title = book_data['Title']
                            publisher = book_data['Publisher']
                            isbn10 = book_data['ISBN-10']
                            isbn13 = book_data['ISBN-13']
                            copies = 1

                            existing_book = self.find_book_by_isbn10(isbn10)  #to make a flag if a book exists already

                            if existing_book:
                                print(f"A book with the ISBN-10 {isbn10} already exists in the library.")
                                choice = input("Do you want to replace the existing record or add a new copy? (replace/add): ")
                                #choosing between replacing or adding another copy of an already existing book
                                if choice.lower() == 'replace':
                                    self.books.remove(existing_book)
                                    book_data.pop("Title")
                                    book_data.pop("Publisher")
                                    book_data.pop("ISBN-10")
                                    book_data.pop("ISBN-13")
                                    book = Book(title, publisher, isbn10,isbn13,copies, **book_data)
                                    self.books.append(book)
                                    print("Book record replaced successfully.")
                                elif choice.lower() == 'add':
                                    existing_book.copies += 1
                                    print("Book copy added successfully.")
                                else:
                                    print("Invalid choice. Book not added.")
                            else:
                                book_data.pop("Title")
                                book_data.pop("Publisher")
                                book_data.pop("ISBN-10")
                                book_data.pop("ISBN-13")
                                book = Book(title, publisher, isbn10,isbn13,copies, **book_data)
                                self.books.append(book)
                                print("Book added successfully.")
                            book_data = {}
                    else:
                        print("Invalid book information. Skipping book.")
        except FileNotFoundError:  #if file is not found
            print("File not found or inaccessible.")


    def search(self, keyword, save_to_file=False): # Searching for a book in the library
        books_found = []
        for book in self.books:  #loop on the existing books to find the wanted book
            book_info = str(book).lower()
            if keyword.lower() in book_info:
                books_found.append(book)

        if books_found:
            print("Search Results:")
            for book in books_found:
                print(book)
            if save_to_file:
                self.save_search(books_found)
                print("Search results saved to file.")
        else:
            print("No books found.")

    def edit(self, identifier):  #Editing a specified Book
        #searches for book according to isbn
        book = self.find_book_by_isbn10(identifier)

        if book:
            print("Book found:")
            print(book)
            choice = input("Do you want to edit this book? (yes/no): ") #Permission needed
            if choice.lower() == "yes":
                # new arguments
                new_title = input("Enter the new title: ")
                new_publisher = input("Enter the new publisher: ")
                new_isbn10 = input("Enter the new ISBN-10: ")
                new_isb13 = input("Enter the new ISBN-13: ")
                new_Copies = input("Enter the new number of copies: ")
                #Assiging new arguments
                book.title = new_title
                book.publisher = new_publisher
                book.isbn10 = new_isbn10
                book.isbn13 = new_isb13
                book.copies = new_Copies

                print("Book information updated successfully.")
        else:
            print("Book not found.")

    def archive(self, identifier):  #Archiving a specified book in the library
        book = self.find_book_by_isbn10(identifier)
        if book:  #found
            print("Book found:")
            print(book)
            choice = input("Do you want to archive this book? (yes/no): ")  #asking for permission
            if choice.lower() == "yes":
                book.archived = True
                print("Book archived successfully.")
        else:
            print("Book not found.")

    def remove(self):  #Removing an Archived Book from the library

        archived_books = [book for book in self.books if book.archived]
        # to check if a book is archived or not
        if not archived_books:
            print("No archived books found.")
            return

        print("Archived Books:")
        for index, book in enumerate(archived_books): # Making an array of archived books
            print(f"{index + 1}. {book}") # printing archived books

        choice = input("Enter the number of the book you want to remove: ")  #removes a boook according to it's index
        try:
            index = int(choice) - 1
            if 0 <= index < len(archived_books):
                book = archived_books[index]
                self.books.remove(book)
                print("Book removed successfully.")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid choice.")

    def generate_LMS_reports(self):  #Making a Report about the books that exists the library
        total_books = sum(book.copies for book in self.books)  # number of total books in the LMS
        unique_books = len(set(book.isbn10 for book in self.books))  #Number of unique books in LMS
        archived_books = sum(book.archived for book in self.books)  #Number of Archived Books in LMS

        year = input("Enter a particular year: ")  #to search for a book after a certain year
        new_books = sum(int(book.extra_info.get('Year', 0)) > int(year) for book in self.books)

        pd = {}  #for publishers
        yd = {}  #for Years

        for book in self.books:
            publisher = book.publisher
            if publisher in pd:
                pd[publisher] += 1
            else:
                pd[publisher] = 1

            book_year = book.extra_info.get('Year')
            if book_year in yd:
                yd[book_year] += 1
            else:
                yd[book_year] = 1

        print("Reports:")
        print(f"Total books in the LMS: {total_books}")
        print(f"Number of unique books in the LMS: {unique_books}")
        print(f"Number of archived books in the LMS: {archived_books}")
        print(f"Number of books in the LMS newer than {year}: {new_books}")
        print("Book Distribution by Publisher:")
        for publisher, count in pd.items():
            print(f"{publisher}: {count}")
        print("Book Distribution by Year:")
        for year, count in yd.items():
            print(f"{year}: {count}")

    def save_search(self, search_results):  #a function that saves the books that are searched
        file = input("Enter the file name to save the search results: ")
        try:
            with open(file, 'w') as File:
                for book in search_results:
                    File.write(str(book))
                    File.write("\n\n")
        except IOError:
            print("Error occurred while saving the search results.")

    def find_book_by_isbn10(self, isbn): #searching for a book through ISBN-10
        for book in self.books:
            if book.isbn10 == isbn:
                return book
        return None

    def menu(self):
        while True:

            print("\nWeolcome to Library Management System\n")
            print("\nMade by Mahdi Abu Arafeh And Ahmad Bakri\n")
            print("1. Adding books from a certain file")
            print("2. Search for books in the Library")
            print("3. Edit a certain book information")
            print("4. Archive a certain book")
            print("5. Remove a certain book")
            print("6. Generate reports about Books in Library")
            print("7. Exit")

            option = input("Enter your choice (1-7): ")

            if option == "1":
                file_path = input("Enter the file path: ")
                self.add(file_path)

            elif option == "2":
                keyword = input("Enter a keyword to search: ")  # a key to search for a book
                save_to_file = input("Do you want to save the search results to a file? (yes/no): ")  # if user wants to save the results
                if save_to_file.lower() == 'yes':
                    self.search(keyword, save_to_file=True)
                else:
                    self.search(keyword)

            elif option == "3":
                identifier = input("Enter the ISBN-10 number of the book to edit: ")  # a key to search for a book
                self.edit(identifier)

            elif option == "4":
                identifier = input("Enter the ISBN-10 number of the book to archive: ")  # a key to search for a book
                self.archive(identifier)

            elif option == "5": #to remove
                self.remove()

            elif option == "6":  # to make report
                self.generate_LMS_reports()

            elif option == "7":
                print("Exiting the program...")
                break

            else:
                print("Invalid choice. Please enter a number from 1 to 7.")