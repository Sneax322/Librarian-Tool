import os
import random
import csv
if not os.path.exists('patron1.csv') or os.path.getsize('patron1.csv') == 0:
    with open('patron1.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'name', 'age', 'library_number', 'fines', 'borrowed_books',
            'days_overdue', 'max_books_allowed', 'max_days_allowed', 'object'
        ])
if not os.path.exists('assistant1.csv') or os.path.getsize('assistant1.csv') == 0:
    with open('assistant1.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'age', 'username', 'password', 'library_number', 'object'])
class Book:
    def __init__(self, title, authors, average_rating, isbn, isbn13, language_code, num_pages, ratings_count, text_reviews_count, publication_date, publisher):
        self.title = title
        self.authors = authors
        self.average_rating = average_rating
        self.isbn = isbn
        self.isbn13 = isbn13
        self.language_code = language_code
        self.num_pages = num_pages
        self.ratings_count = ratings_count
        self.text_reviews_count = text_reviews_count
        self.publication_date = publication_date
        self.publisher = publisher

books = []

with open('books.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Strip whitespace from column names and handle None values
        clean_row = {k.strip(): (v.strip() if v and isinstance(v, str) else v) for k, v in row.items() if k}
        
        # Skip if missing critical fields
        if not clean_row.get('title') or not clean_row.get('isbn'):
            continue
        
        try:
            book = Book(
                title = clean_row.get('title', ''),
                authors = clean_row.get('authors', ''),
                average_rating = float(clean_row.get('average_rating', 0)) if clean_row.get('average_rating') else 0.0,
                isbn = clean_row.get('isbn', ''),
                isbn13 = clean_row.get('isbn13', ''),
                language_code = clean_row.get('language_code', ''),
                num_pages = int(clean_row.get('num_pages', 0)) if clean_row.get('num_pages') else 0,
                ratings_count = int(clean_row.get('ratings_count', 0)) if clean_row.get('ratings_count') else 0,
                text_reviews_count = int(clean_row.get('text_reviews_count', 0)) if clean_row.get('text_reviews_count') else 0,
                publication_date = clean_row.get('publication_date', ''),
                publisher = clean_row.get('publisher', '')
            )
            books.append(book)
        except (ValueError, KeyError):
            continue

used_library_numbers = set()
def generate_library_number():
    while True:
        num = random.randint(10000, 99999)  # 5-digit number
        if num not in used_library_numbers:
            used_library_numbers.add(num)
            return num
# librarians=[]
# assistants=[]
# students=[]
# faculties=[]
# communities=[]
# child=[]
class Person:#DONE
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Staff(Person):
    def __init__(self, name, age, username, password):
        super().__init__(name, age)
        self.username=username
        self.password=password
        #ADD ATTRIBUTES AND METHODS COMMON IN ASSISTANT AND LIBRARY
        #COMMON METHODS
    def delete_own_account(self):
        pass
    def add_fines(self,patron):
        pass
    def calculate_fines(self,patron):
        pass
    def lend_book(self):
        pass
    def receive_book(self,patron):
        pass
    def report(self):
        pass


class Librarian(Staff):
    def __repr__(self):
        return f'Librarian({self.name}, {self.age}, {self.username})'
    def add_assistant(): #DONE
        name = input("Enter assistant's name: ")
        age = int(input("Enter assistant's age: "))
        while True:
            username = input("Enter assistant's username: ")
            with open('assistant1.csv', mode='r', newline='') as file:
                reader = csv.DictReader(file)
                if any(row['username'] == username for row in reader):
                    print("Username already exists. Please choose a different username.\n")
                else:
                    break
        password = input("Enter assistant's password: ")
        new_assistant = Assistant(name, age, username, password)
        with open('assistant1.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, age, username, password])

    def remove_assistant(self, username):
       librarian.show_assistants_info()
       username = input("Enter the username of the assistant to remove: ")
         with open('assistant1.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            assistants = list(reader)
        with open('assistant1.csv', mode='w', newline='') as file:
            fieldnames = ['name', 'age', 'username', 'password', 'library_number', 'object']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            removed = False
            for assistant in assistants:
                if assistant['username'] != username:
                    writer.writerow(assistant)
                else:
                    removed = True
            if removed:
                print(f'Assistant with username {username} removed successfully.')
            else:
                print(f'Assistant with username {username} not found.')
    
    
    def show_assistants_info(self):
        with open('assistant1.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            assistants = list(reader)
            if not assistants:
                print("No assistants available.")
                return
            for assistant in assistants:
                print(f"Name: {assistant['name']}, Age: {assistant['age']}, Username: {assistant['username']}")

#ADD_PATRON HAS BEEN CHECKED THOROUGHLY BUT PUT VALIDATION ON OUTER CODE LIKE AGE ETC
    def add_patron(self):#DONE
        choice=int(choice)
        name = input("Enter patron's name: ")   
        age = int(input("Enter patron's age: "))
        library_number = generate_library_number()
        if choice == 1:  # Student
            new_patron = Student(name, age, library_number, max_books_allowed=5, max_days_allowed=30)
            print(f'Student added with library number: {library_number}')
        elif choice == 2:  # Faculty
            new_patron = Faculty(name, age, library_number, max_books_allowed=10, max_days_allowed=60)
            print(f'Faculty added with library number: {library_number}')
        elif choice == 3:  # Community
            new_patron = Community(name, age, library_number, max_books_allowed=3, max_days_allowed=20)
            print(f'Community member added with library number: {library_number}')
        elif choice == 4:  
            while True:
                if age > 12:
                    print("Age exceeds the limit for Child patron type.  ")
                    age = int(input("Enter a valid age (12 or below)."))
                else:
                    break
            new_patron = Child(name, age, library_number, max_books_allowed=2, max_days_allowed=15)
            print(f'Child added with library number: {library_number}')
        with open('patron1.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                new_patron.name, new_patron.age, new_patron.library_number, new_patron.fines,
                new_patron.borrowed_books, new_patron.days_overdue, new_patron.max_books_allowed,
                new_patron.max_days_allowed, repr(new_patron)
            ])
        
#REMOVE_PATRON HAS BEEN CHECKED THOROUGHLY 
    def remove_patron():#DONE
        librarian.show_patrons_info()
        library_number = int(input("Enter the library number of the patron to remove: "))
        if library_number not in used_library_numbers:
            print('Library number does not exist.')
            return
        with open('patron1.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            patrons = list(reader)
        with open('patron1.csv', mode='w', newline='') as file:
            fieldnames = ['name', 'age', 'library_number', 'fines', 'borrowed_books',
                          'days_overdue', 'max_books_allowed', 'max_days_allowed', 'object']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            removed = False
            for patron in patrons:
                if int(patron['library_number']) != library_number:
                    writer.writerow(patron)
                else:
                    removed = True
            if removed:
                used_library_numbers.remove(library_number)
                print(f'Patron with library number {library_number} removed successfully.')
            else:
                print(f'Patron with library number {library_number} not found.')
        
        
    def show_patrons_info(self):#DONE
        with open('patron1.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            patrons = list(reader)
            if not patrons:
                print("No patrons available.")
                return
            for patron in patrons:
                print(f"Name: {patron['name']}, Age: {patron['age']}, Library Number: {patron['library_number']}, Fines: {patron['fines']}, Borrowed Books: {patron['borrowed_books']}, Days Overdue: {patron['days_overdue']}, Max Books Allowed: {patron['max_books_allowed']}, Max Days Allowed: {patron['max_days_allowed']}")

    def edit_patron_info(self):
            

           
    


    
    def add_book(self, title, author, isbn):
        print("Add a book")
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        isbn = input("Enter book ISBN: ")
        isbn13 = input("Enter book ISBN-13: ")
        language_code = input("Enter book language code: ")
        num_pages = input("Enter number of pages: ")
        ratings_count = input("Enter ratings count: ")
        text_reviews_count = input("Enter text reviews count: ")
        publication_date = input("Enter book publication date: ")
        publisher = input("Enter book publisher: ")

        for book in books:
            if book.isbn == isbn:
                print("Book with this ISBN already exists in the library.")
                return
    def remove_book(self):
        pass
    



class Assistant(Staff):
 def __repr__(self):
        return f'Assistant({self.name}, {self.age}, {self.username})'
class Patron(Person):
    def __init__(self, name, age,library_number, fines=0.0 ,borrowed_books=None,days_overdue=0, max_books_allowed=0, max_days_allowed=0):
        super().__init__(name, age)
        self.fines=fines
        self.borrowed_books=borrowed_books if borrowed_books is not None else {}
        self.days_overdue=days_overdue
        self.max_books_allowed=max_books_allowed
        self.max_days_allowed=max_days_allowed
        self.library_number=library_number
    def __repr__(self):
        return f'Patron({self.name}, {self.age}, {self.library_number})'
        #ADD ATTRIBUTES AND METHODS COMMON IN PATRON TYPES
    
class Student(Patron):
     def __init__(self, name, age, library_number):
        super().__init__(name, age, library_number, max_books_allowed=5, max_days_allowed=30)
     def __repr__(self):
        return f'Student({self.name},{self.age})'
class Faculty(Patron):
     def __init__(self, name, age, library_number):
        super().__init__(name, age, library_number, max_books_allowed=10, max_days_allowed=60)
     def __repr__(self):
        return f'Faculty({self.name},{self.age})'
    

class Community(Patron):
    def __init__(self, name, age, library_number):
        super().__init__(name, age, library_number, max_books_allowed=3, max_days_allowed=20)
    def __repr__(self):
        return f'Community({self.name},{self.age})'

class Child(Patron):
    def __init__(self, name, age, library_number):
        super().__init__(name, age, library_number, max_books_allowed=2, max_days_allowed=15)
    def __repr__(self):
        return f'Child({self.name},{self.age})'

def menu_5_1():#MENU 5.1 ADD PATRON
    print("Select Patron Type to Add:")
    print("1. Student")
    print("2. Faculty")
    print("3. Community")
    print("4. Child")
    #ILAGAY YUNG CURRENTUSER.ADDPATRON LATER ON