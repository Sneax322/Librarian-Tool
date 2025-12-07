import datetime
import os
import random
import csv
import json
import pandas as pd
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
if not os.path.exists('librarian1.csv') or os.path.getsize('librarian1.csv') == 0:
    with open('librarian1.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'age', 'username', 'password', 'library_number', 'object'])


def clear_screen():
   
    if os.name == 'nt':
        os.system('cls')

    else:
     os.system('clear')


current_user=None
current_client=None
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

with open('books123.updated.csv', mode='r', encoding='utf-8') as file:
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
    def add_book(self):#DONE
        clear_screen()
        print("Add a book")
        title = input("Enter book title: ")
        authors = input("Enter book author(s): ")
        isbn = input("Enter book ISBN: ")
        
        # Check if ISBN already exists
        for book in books:
            if book.isbn == isbn:
                print("Book with this ISBN already exists in the library.")
                return

        isbn13 = input("Enter book ISBN-13: ")
        language_code = input("Enter book language code: ")
        
        try:
            num_pages = int(input("Enter number of pages: "))
        except ValueError:
            num_pages = 0

        try:
            ratings_count = int(input("Enter ratings count: "))
        except ValueError:
            ratings_count = 0

        try:
            text_reviews_count = int(input("Enter text reviews count: "))
        except ValueError:
            text_reviews_count = 0

        publication_date = input("Enter book publication date: ")
        publisher = input("Enter book publisher: ")

        max_book_id = 0
        with open('books123.updated.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    book_id = int(row.get('bookID', 0))
                    if book_id > max_book_id:
                        max_book_id = book_id
                except ValueError:
                    continue

        next_book_id = max_book_id + 1

        new_book = Book(title, authors, 0.0, isbn, isbn13, language_code, num_pages, ratings_count, text_reviews_count, publication_date, publisher)
        books.append(new_book)

        with open('books123.updated.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['bookID', 'title', 'authors', 'average_rating', 'isbn', 'isbn13', 'language_code', 'num_pages', 'ratings_count', 'text_reviews_count', 'publication_date', 'publisher', 'Status', 'Checkouts'])
            writer.writerow({
                'bookID': next_book_id,
                'title': title,
                'authors': authors,
                'average_rating': 0.0,
                'isbn': isbn,
                'isbn13': isbn13,
                'language_code': language_code,
                'num_pages': num_pages,
                'ratings_count': ratings_count,
                'text_reviews_count': text_reviews_count,
                'publication_date': publication_date,
                'publisher': publisher,
                'Status': 'Available',
                'Checkouts': 0
            })

        print(f"Book '{title}' added successfully with Book ID: {next_book_id}!")
        
    def remove_book(self):#DONE
        import shutil, os, csv, tempfile
        src = 'books123.updated.csv'
        if not os.path.exists(src):
            print("Books file not found.")
            return

        book_id = input("Enter Book ID to remove (or B to cancel): ").strip()
        if not book_id or book_id.lower() == 'b':
            print("Aborted.")
            return

        # backup
        bak = src + '.bak'
        try:
            shutil.copy2(src, bak)
        except Exception:
            pass

        # read raw CSV
        with open(src, mode='r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            try:
                header = next(reader)
            except StopIteration:
                print("CSV is empty.")
                return
            rows = [row for row in reader]

        id_col = 0
        for i, h in enumerate(header):
            if h and h.strip().lower() == 'bookid':
                id_col = i
                break

        matches = [ (i, r) for i, r in enumerate(rows) if len(r) > id_col and r[id_col].strip() == book_id ]
        if not matches:
            print(f"Book ID '{book_id}' not found.")
            return

        title_col = next((i for i,h in enumerate(header) if h and h.strip().lower() == 'title'), None)
        isbn_col  = next((i for i,h in enumerate(header) if h and h.strip().lower() == 'isbn'), None)
        for idx, r in matches:
            title = r[title_col] if title_col is not None and title_col < len(r) else ''
            isbn =  r[isbn_col]  if isbn_col  is not None and isbn_col  < len(r) else ''
            print(f"  row_index={idx}  bookID={r[id_col]}  title={title[:80]}  isbn={isbn}")

        if input("Confirm removal of these record(s)? (y/N): ").strip().lower() != 'y':
            print("Aborted.")
            return

        remove_indices = {i for i, _ in matches}
        updated_rows = [r for i, r in enumerate(rows) if i not in remove_indices]

        fd, tmp = tempfile.mkstemp(prefix='books_', suffix='.csv', dir='.')
        os.close(fd)
        try:
            with open(tmp, mode='w', encoding='utf-8', newline='') as out:
                writer = csv.writer(out)
                writer.writerow([h for h in header if h is not None])
                writer.writerows(updated_rows)
            os.replace(tmp, src)
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)

        removed_isbns = set()
        for _, r in matches:
            if isbn_col is not None and isbn_col < len(r):
                removed_isbns.add(r[isbn_col].strip())
        global books
        books[:] = [b for b in books if (b.isbn or '').strip() not in removed_isbns]

        print(f"Removed {len(remove_indices)} record(s).")
    def delete_own_account(self):
        pass
    def add_fines(self,patron):
        pass
    def calculate_fines(self,patron):
        pass
    def lend_book(self):
        import tempfile, os, csv, json, datetime
        clear_screen()
        print("Lend a Book")
        lib_input = input("Enter patron library number (or B to cancel): ").strip()
        if not lib_input or lib_input.lower() == 'b':
            print("Aborted.")
            return
        try:
            library_number = int(lib_input)
        except ValueError:
            print("Invalid library number.")
            return
        
        p_path = 'patron1.csv'
        if not os.path.exists(p_path):
            print("Patron file not found.")
            return
        with open(p_path, mode='r', encoding='utf-8', newline='') as pfile:
            preader = csv.DictReader(pfile)
            p_fieldnames = preader.fieldnames or ['name','age','library_number','fines','borrowed_books','days_overdue','max_books_allowed','max_days_allowed','object']
            patrons = list(preader)

        patron = None
        for p in patrons:
            try:
                if int(p.get('library_number', -1)) == library_number:
                    patron = p
                    break
            except Exception:
                continue
        if not patron:
            print(f"Patron with library number {library_number} not found.")
            return

        bb_raw = patron.get('borrowed_books') or '{}'
        try:
            borrowed = json.loads(bb_raw) if isinstance(bb_raw, str) else borrowed
        except Exception:
            try:
                import ast
                borrowed = ast.literal_eval(bb_raw)
            except Exception:
                borrowed = {}

        try:
            max_allowed = int(patron.get('max_books_allowed') or 0)
        except Exception:
            max_allowed = 0
        if max_allowed and len(borrowed) >= max_allowed:
            print("Patron has reached the maximum allowed borrowed books.")
            return

        book_id = input("Enter Book ID to lend (or B to cancel): ").strip()
        if not book_id or book_id.lower() == 'b':
            print("Aborted.")
            return

        books_path = 'books123.updated.csv'
        if not os.path.exists(books_path):
            print("Books file not found.")
            return

        with open(books_path, mode='r', encoding='utf-8', newline='') as bfile:
            breader = csv.DictReader(bfile)
            raw_b_fieldnames = breader.fieldnames or ['bookID','title','authors','average_rating','isbn','isbn13','language_code','num_pages','ratings_count','text_reviews_count','publication_date','publisher','Status','Checkouts']
            b_fieldnames = [fn for fn in raw_b_fieldnames if fn and str(fn).strip()]
            books_rows = list(breader)

        match = None
        for row in books_rows:
            if (row.get('bookID') or '').strip() == book_id:
                match = row
                break
        if not match:
            print(f"Book ID {book_id} not found.")
            return

        status = (match.get('Status') or match.get('status') or '').strip()
        if status.lower() == 'checked out':
            print("Book is already checked out.")
            return

        match['Status'] = 'Checked Out'
        try:
            current_checkouts = int((match.get('Checkouts') or '0').strip())
        except Exception:
            current_checkouts = 0
        match['Checkouts'] = str(current_checkouts + 1)

        fd, tmp_path = tempfile.mkstemp(prefix='books_', suffix='.csv', dir='.')
        os.close(fd)
        try:
            with open(tmp_path, mode='w', encoding='utf-8', newline='') as out:
                writer = csv.DictWriter(out, fieldnames=b_fieldnames)
                writer.writeheader()
                sanitized_rows = []
                for row in books_rows:
                    clean_row = {fn: (row.get(fn, '') if row.get(fn) is not None else '') for fn in b_fieldnames}
                    sanitized_rows.append(clean_row)
                writer.writerows(sanitized_rows)
            os.replace(tmp_path, books_path)
        finally:
            if os.path.exists(tmp_path):
                try: os.remove(tmp_path)
                except Exception: pass

        isbn_key = (match.get('isbn') or match.get('isbn13') or '').strip() or book_id
        today = datetime.date.today()
        try:
            max_days = int(patron.get('max_days_allowed') or 0)
        except Exception:
            max_days = 0
        due_date = (today + datetime.timedelta(days=max_days)).isoformat() if max_days > 0 else ''

        borrowed[isbn_key] = {'checkout_date': today.isoformat(), 'due_date': due_date, 'bookID': book_id}
        patron['borrowed_books'] = json.dumps(borrowed)

        fd2, tmp2 = tempfile.mkstemp(prefix='patrons_', suffix='.csv', dir='.')
        os.close(fd2)
        try:
            with open(tmp2, mode='w', encoding='utf-8', newline='') as p_out:
                writer = csv.DictWriter(p_out, fieldnames=p_fieldnames)
                writer.writeheader()
                writer.writerows(patrons)
            os.replace(tmp2, p_path)
        finally:
            if os.path.exists(tmp2):
                try: os.remove(tmp2)
                except Exception: pass

        global books
        for b in books:
            if getattr(b, 'isbn', '') == match.get('isbn') or getattr(b, 'isbn13', '') == match.get('isbn13') or getattr(b, 'title', '') == match.get('title'):
                try:
                    b.Status = 'Checked Out'
                    b.Checkouts = int(getattr(b, 'Checkouts', 0)) + 1
                except Exception:
                    pass

        print(f"Book ID {book_id} lent to patron {library_number}. Due: {due_date}")
    def receive_book(self):
        import tempfile, os, csv, json, datetime
        clear_screen()
        print("Receive a Returned Book")
        
        book_id = input("Enter Book ID being returned (or B to cancel): ").strip()
        if not book_id or book_id.lower() == 'b':
            print("Aborted.")
            return

        books_path = 'books123.updated.csv'
        if not os.path.exists(books_path):
            print("Books file not found.")
            return

        with open(books_path, mode='r', encoding='utf-8', newline='') as bfile:
            breader = csv.DictReader(bfile)
            raw_b_fieldnames = breader.fieldnames or ['bookID','title','authors','average_rating','isbn','isbn13','language_code','num_pages','ratings_count','text_reviews_count','publication_date','publisher','Status','Checkouts']
            b_fieldnames = [fn for fn in raw_b_fieldnames if fn and str(fn).strip()]
            books_rows = list(breader)

        match = None
        for row in books_rows:
            if (row.get('bookID') or '').strip() == book_id:
                match = row
                break
        if not match:
            print(f"Book ID {book_id} not found.")
            return

        status = (match.get('Status') or match.get('status') or '').strip()
        if status.lower() == 'available':
            print("Book is already available (not checked out).")
            return

        match['Status'] = 'Available'

        fd, tmp_path = tempfile.mkstemp(prefix='books_', suffix='.csv', dir='.')
        os.close(fd)
        try:
            with open(tmp_path, mode='w', encoding='utf-8', newline='') as out:
                writer = csv.DictWriter(out, fieldnames=b_fieldnames)
                writer.writeheader()
                sanitized_rows = []
                for row in books_rows:
                    clean_row = {fn: (row.get(fn, '') if row.get(fn) is not None else '') for fn in b_fieldnames}
                    sanitized_rows.append(clean_row)
                writer.writerows(sanitized_rows)
            os.replace(tmp_path, books_path)
        finally:
            if os.path.exists(tmp_path):
                try: os.remove(tmp_path)
                except Exception: pass

        p_path = 'patron1.csv'
        if os.path.exists(p_path):
            with open(p_path, mode='r', encoding='utf-8', newline='') as pfile:
                preader = csv.DictReader(pfile)
                p_fieldnames = preader.fieldnames or ['name','age','library_number','fines','borrowed_books','days_overdue','max_books_allowed','max_days_allowed','object']
                patrons = list(preader)

            isbn_key = (match.get('isbn') or '').strip()
            removed = False
            for p in patrons:
                bb_raw = p.get('borrowed_books') or '{}'
                try:
                    borrowed = json.loads(bb_raw) if isinstance(bb_raw, str) else borrowed
                except Exception:
                    try:
                        import ast
                        borrowed = ast.literal_eval(bb_raw)
                    except Exception:
                        borrowed = {}
                
                if isbn_key in borrowed:
                    del borrowed[isbn_key]
                    p['borrowed_books'] = json.dumps(borrowed)
                    removed = True

            if removed:
                fd2, tmp2 = tempfile.mkstemp(prefix='patrons_', suffix='.csv', dir='.')
                os.close(fd2)
                try:
                    with open(tmp2, mode='w', encoding='utf-8', newline='') as p_out:
                        writer = csv.DictWriter(p_out, fieldnames=p_fieldnames)
                        writer.writeheader()
                        writer.writerows(patrons)
                    os.replace(tmp2, p_path)
                finally:
                    if os.path.exists(tmp2):
                        try: os.remove(tmp2)
                        except Exception: pass

        print(f"Book ID {book_id} received and marked Available.")
    def report(self):
        pass
    @classmethod
    def show_patrons_info(cls):#DONE
        with open('patron1.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            patrons = list(reader)
            if not patrons:
                print("No patrons available.")
                return
            for patron in patrons:
                print(f"Name: {patron['name']}, Age: {patron['age']}, Library Number: {patron['library_number']}, Fines: {patron['fines']}, Borrowed Books: {patron['borrowed_books']}, Days Overdue: {patron['days_overdue']}, Max Books Allowed: {patron['max_books_allowed']}, Max Days Allowed: {patron['max_days_allowed']}")


class Librarian(Staff):
    def __repr__(self):
        return f'Librarian({self.name}, {self.age}, {self.username})'
    @classmethod
    def add_librarian(cls):#DONE
        clear_screen()
        name = input("Enter librarian's name: ")
        age = int(input("Enter librarian's age: "))
        while True:
            username = input("Enter librarian's username: ")
            with open('librarian1.csv', mode='r', newline='') as file:
                reader = csv.DictReader(file)
                if any(row['username'] == username for row in reader):
                    print("Username already exists. Please choose a different username.\n")
                else:
                    break
        password = input("Enter librarian's password: ")
        new_librarian = Librarian(name, age, username, password)
        with open('librarian1.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, age, username, password])
    # def edit_book_status(self):
    #     choice=int(input("Enter choice: "))
    #     if choice==1 or choice==2 or choice==3:
    #         user=input( "Enter the library number of the patron you are transacting with." )
    #         current_client= None
    #         with open('patron1.csv', mode='r', newline='', encoding='utf-8') as pfile:
    #             preader = csv.DictReader(pfile)
    #             for patron in preader:
    #                 try:
    #                     if int(patron.get('library_number', -1)) == int(user):
    #                         current_client=patron
    #                         break
    #                 except ValueError:
    #                     continue
    #     if choice==1:
    #         current_client.book
    #         #i want current client to be patron object
    #         #like current_client= is the patron object that matches the library number
        
    #     with open('books123.updated.csv', mode='r', newline='', encoding='utf-8') as file:
    #         reader = csv.DictReader(file)
    #         books = list(reader)            
    #     with open('books123.updated.csv', mode='w', newline='', encoding='utf-8') as file:
    #         fieldnames = reader.fieldnames
    #         writer = csv.DictWriter(file, fieldnames=fieldnames)
    #         writer.writeheader()
    #         for book in books:
    #             if choice == 1:
    #                 book['status'] = 'Available'
    #             elif choice == 2:
    #                 book['status'] = 'Checked Out'#suggest add code to add checkouts+1

                    

                    
    #             elif choice == 3:
    #                 book['status'] = 'Reserved'

    #             elif choice == 4:
    #                 book['status'] = 'Lost'
    #             writer.writerow(book)

    # def edit_book_status_and_update_patron(self):
    #     """Improved edit: change a single book by ISBN and optionally update the patron record.
    #     This stores `borrowed_books` in `patron1.csv` as a JSON string mapping ISBN -> info.
    #     """
    #     choice = int(input("Enter choice: \n1. Available\n2. Checked Out\n3. Reserved\n4. Lost\nChoice: "))

    #     isbn = input("Enter the ISBN (or ISBN13) of the book to change: ").strip()
    #     patron_lib_input = None
    #     if choice in (1, 2, 3):
    #         patron_lib_input = input("Enter the library number of the patron you are transacting with (or press Enter to skip): ").strip()

    #     # Update book status in books CSV
    #     with open('books123.updated.csv', mode='r', newline='', encoding='utf-8') as file:
    #         reader = csv.DictReader(file)
    #         books = list(reader)
    #         fieldnames = reader.fieldnames

    #     updated = False
    #     for book in books:
    #         if (book.get('isbn') and book.get('isbn').strip() == isbn) or (book.get('isbn13') and book.get('isbn13').strip() == isbn):
    #             if choice == 1:
    #                 book['status'] = 'Available'
    #             elif choice == 2:
    #                 book['status'] = 'Checked Out'
    #                 book['checkouts'] = str(int(book.get('checkouts') or 0) + 1)
    #             elif choice == 3:
    #                 book['status'] = 'Reserved'
    #             elif choice == 4:
    #                 book['status'] = 'Lost'
    #             updated = True
    #             break

    #     if not updated:
    #         print(f"No book with ISBN {isbn} found in books CSV.")

    #     with open('books123.updated.csv', mode='w', newline='', encoding='utf-8') as file:
    #         writer = csv.DictWriter(file, fieldnames=fieldnames)
    #         writer.writeheader()
    #         for b in books:
    #             writer.writerow(b)

    #     # Update patron record if provided
    #     if patron_lib_input:
    #         try:
    #             library_number = int(patron_lib_input)
    #         except ValueError:
    #             print('Invalid library number provided; skipping patron update.')
    #             return

    #         with open('patron1.csv', mode='r', newline='', encoding='utf-8') as pfile:
    #             preader = csv.DictReader(pfile)
    #             patrons = list(preader)
    #             p_fieldnames = preader.fieldnames

    #         patron_found = False
    #         for patron in patrons:
    #             try:
    #                 if int(patron.get('library_number', -1)) == library_number:
    #                     patron_found = True
    #                     bb_raw = patron.get('borrowed_books') or '{}'
    #                     try:
    #                         borrowed = json.loads(bb_raw) if isinstance(bb_raw, str) else {}
    #                     except Exception:
    #                         borrowed = {}

    #                     today = datetime.date.today()
    #                     if choice == 2:
    #                         max_days = int(patron.get('max_days_allowed') or 0)
    #                         due = (today + datetime.timedelta(days=max_days)).isoformat()
    #                         borrowed[isbn] = {'status': 'checked_out', 'due_date': due, 'checkout_date': today.isoformat()}
    #                     elif choice == 1:
    #                         if isbn in borrowed:
    #                             del borrowed[isbn]
    #                     elif choice == 3:
    #                         borrowed[isbn] = {'status': 'reserved', 'reserved_date': today.isoformat()}

    #                     patron['borrowed_books'] = json.dumps(borrowed)
    #                     break
    #             except ValueError:
    #                 continue

    #         if not patron_found:
    #             print(f'Patron with library number {library_number} not found; patron CSV not updated.')
    #             return

    #         with open('patron1.csv', mode='w', newline='', encoding='utf-8') as pfile:
    #             writer = csv.DictWriter(pfile, fieldnames=p_fieldnames)
    #             writer.writeheader()
    #             for pat in patrons:
    #                 writer.writerow(pat)
    #         print('Book status and patron record updated.')

    def add_assistant(self): #DONE
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

    def remove_assistant(self):
       clear_screen()
       self.show_assistants_info()
       username = input("Enter the username of the assistant to remove/Press B to go cancel: ")
       if username.lower() == 'b':
        return
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
        clear_screen()
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
        while True:
         choice=input("Enter your choice: ")
         if choice.isdigit() and 1 <= int(choice) <= 4:
                break
         else:
                print("Invalid choice. Please enter a number between 1 and 4.")
        name = input("Enter patron's name: ")
        while True:
         try:
          age = int(input("Enter patron's age: "))
          if age < 0:
            print("Age cannot be negative.")
            continue
          break
         except ValueError:
          print("Please enter a valid integer for age.")
        library_number = generate_library_number()
        if choice == "1":  # Student
            new_patron = Student(name, age, library_number)
            print(f'Student added with library number: {library_number}')
        elif choice == "2":  # Faculty
            new_patron = Faculty(name, age, library_number)
            print(f'Faculty added with library number: {library_number}')
        elif choice == "3":  # Community
            new_patron = Community(name, age, library_number)
            print(f'Community member added with library number: {library_number}')
        elif choice == "4":
            while True:
                if age > 12:
                    print("Age exceeds the limit for Child patron type.  ")
                    age = int(input("Enter a valid age (12 or below)."))
                else:
                    break
            new_patron = Child(name, age, library_number)
            print(f'Child added with library number: {library_number}')
        with open('patron1.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                new_patron.name, new_patron.age, new_patron.library_number, new_patron.fines,
                new_patron.borrowed_books, new_patron.days_overdue, new_patron.max_books_allowed,
                new_patron.max_days_allowed, repr(new_patron)
            ])
        
#REMOVE_PATRON HAS BEEN CHECKED THOROUGHLY 
    def remove_patron(self):#DONE
        clear_screen()
        current_user.show_patrons_info()
        lib_input = input("Enter the library number of the patron to remove/Press B to cancel: ")
        if lib_input.lower() == 'b':
            return
        try:
            library_number = int(lib_input)
        except ValueError:
            print("Invalid library number. Please enter a numeric value.")
            return

        
        with open('patron1.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            patrons = list(reader)

        if not any(int(p.get('library_number', -1)) == library_number for p in patrons):
            print('Library number does not exist.')
            return

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
            used_library_numbers.discard(library_number)
            print(f'Patron with library number {library_number} removed successfully.')
        else:
            print(f'Patron with library number {library_number} not found.')

    # def remove_patron(self):#DONE
    #     clear_screen()
    #     current_user.show_patrons_info()
    #     library_number = input("Enter the library number of the patron to remove/Press B to cancel: ")
    #     if library_number.lower() == 'b':
    #         return
    #     if library_number not in used_library_numbers:
    #         print('Library number does not exist.')
    #         return
    #     with open('patron1.csv', mode='r', newline='') as file:
    #         reader = csv.DictReader(file)
    #         patrons = list(reader)
    #     with open('patron1.csv', mode='w', newline='') as file:
    #         fieldnames = ['name', 'age', 'library_number', 'fines', 'borrowed_books',
    #                       'days_overdue', 'max_books_allowed', 'max_days_allowed', 'object']
    #         writer = csv.DictWriter(file, fieldnames=fieldnames)
    #         writer.writeheader()
    #         removed = False
    #         for patron in patrons:
    #             if int(patron['library_number']) != library_number:
    #                 writer.writerow(patron)
    #             else:
    #                 removed = True
    #         if removed:
    #             used_library_numbers.remove(library_number)
    #             print(f'Patron with library number {library_number} removed successfully.')
    #         else:
    #             print(f'Patron with library number {library_number} not found.')
        
        
    

    def edit_patron_info(self):
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
    
def first_menu():#FIRST TIME MENU(if currentuser=none)
    global current_user
    print("Welcome to the Library Management System")
    print("Since there is no accounts yet, please create your librarian account to get started.")
    Librarian.add_librarian()
    with open('librarian1.csv', mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            current_user = Librarian(row['name'], int(row['age']), row['username'], row['password'])
            print(f"Account created successfully. Welcome, {current_user.name}!")
    enter=input("Press Enter to continue to the menu.")
    clear_screen()
    librarian_menu()
    
            
            

def login_menu():#LOGIN MENU
    global current_user
    print("Welcome to the Library Management System")
    print("Please log in to continue.")
    print("1. Librarian Login")
    print("2. Assistant Login")
    print("3. Exit\n")
    while True:
        choice=input("Enter your choice: ")
        
        if choice in ['1', '2', '3']:
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")
    if choice == '1':
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        with open('librarian1.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username and row['password'] == password:
                    current_user = Librarian(row['name'], int(row['age']), row['username'], row['password'])
                    print(f"Login successful. Welcome, {current_user.name}!")
                    
                    librarian_menu()
                    return
            print("Invalid username or password. Please try again.\n")
            
    elif choice == '2':
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        with open('assistant1.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username and row['password'] == password:
                    current_user = Assistant(row['name'], int(row['age']), row['username'], row['password'])
                    print(f"Login successful. Welcome, {current_user.name}!")
                    
                    assistant_menu()
                    return
            print("Invalid username or password. Please try again.\n")
            
    elif choice == '3':
        print("Exiting the system. Goodbye!")
        exit()
    
  
            
    
    #add account method
def librarian_menu():#MAIN MENU
    global current_user, current_client
    
    while True:
     clear_screen()
     print("Welcome to the Library Management System")
     print("\n====== Librarian Menu ======\n")
     print("1. Add Book")
     print("2. Remove Book")
     print('3. Lend Book/Receive Book/Edit book status')
     print("4. Show Patron Info")#DONE!
     print('5. Receive fines from Patron')
     print("6. Add Assistant")#DONE
     print("7. Show Assistants")#DOne
     print("8. Remove Assistant")#DOne
     print("9. Add Librarian")#DOne
     print("10. Add Patron")#DOne
     print("11. Remove Patron")#DOne
     print("12. Edit Patron Info")
     print('13. Receive fines from Patron')
     print("14. Calculate Overall Fines")
     print("15. Delete Own Account")
     print("16. Generate Report")
     print('17. Search Books')
     print("18. Logout")
     print('19. Change password/Account info')
     print("0. Exit\n")
     while True:
        next_choice=input("Enter your choice: ")
        if next_choice.isdigit() and 0 <= int(next_choice) <= 18:
            break
        else:
            print("Invalid choice. Please enter a number between 0 and 18.")
     if next_choice=='1': #RESTY
        clear_screen()
        current_user.add_book()
        enter=input("Press Enter to return to the menu.")
        clear_screen()
        continue
     if next_choice=='2':#RESTY
        clear_screen()
        current_user.remove_book()
        enter=input("Press Enter to return to the menu.")
        clear_screen()
        continue
     if next_choice=='3':
        clear_screen()
        print("1. Lend Book")
        print("2. Receive Book")
        print("3. Edit Book Status")
        while True:
         choice=input("Enter your choice: ")
         if choice.isdigit() and 1 <= int(choice) <= 3:
                break
         else:
                print("Invalid choice. Please enter a number between 1 and 3.")
        if choice=='1':
            current_user.lend_book()
            enter=input("Press Enter to return to the menu.")
            clear_screen()
            continue
        if choice=='2':
            current_user.receive_book()
            enter=input("Press Enter to return to the menu.")
            clear_screen()
            continue
        if choice=='3':
            clear_screen()
            menu6_1()
            current_user.edit_book_status_and_update_patron()
            enter=input("Press Enter to return to the menu.")
            clear_screen()
            continue
     if next_choice=='4':#DONE
        clear_screen()
        current_user.show_patrons_info()
        enter=input("Press Enter to return to the menu.")
        clear_screen()
        continue
     if next_choice=='5':
        pass
     if next_choice=='6':
        clear_screen()
        current_user.add_assistant()
        enter=input("Press Enter to return to the menu.")
        clear_screen()
        continue
     if next_choice=='7':
        clear_screen()
        current_user.show_assistants_info()
        enter=input("Press Enter to return to the menu.")
        clear_screen()
        continue
     if next_choice=='8':
        clear_screen()
        current_user.remove_assistant()
        enter=input("Press Enter to return to the menu.")
        clear_screen()
        continue
     if next_choice=='9':
        clear_screen()
        current_user.add_librarian()
        enter=input("Press Enter to return to the menu.")
        clear_screen()
        continue
     if next_choice=='10':
        clear_screen()
        menu_10_1()
        current_user.add_patron()
        enter=input("Press Enter to return to the menu.")
        clear_screen()
        continue
     if next_choice=='11':
        clear_screen()
        current_user.remove_patron()
        enter=input("Press Enter to return to the menu.")
        clear_screen()
        continue
     if next_choice=='12':
        pass
     if next_choice=='13':
        pass
     if next_choice=='14':
        pass
     if next_choice=='15':
        pass
     if next_choice=='16':
        pass
     if next_choice=='17':#RESTY
        pass
     if next_choice=='18':
       clear_screen()
       current_user=None
       clear_screen()
       login_menu()
       break

     if next_choice=='19':
        pass
     if next_choice=='0':
        print("Thank you for using the Library Management System. Goodbye!")
        exit()
    #OPTIONAL TRANSACTION HISTORY

    
def assistant_menu():
    global current_user, current_client
    
    while True:
     clear_screen()
     print("Welcome to the Library Management System")
     print("\n====== Assistant Menu ======\n")
     print("1. Add Book")
     print("2. Remove Book")
     print("3. Lend Book/Receive Book/Edit book status")
     print("4. Show Patron Info")
     print("5. Receive fines from Patron")
     print("6. Delete Own Account")
     print("7. Search Books")
     print("8. Logout")
     print("0. Exit\n")
     while True:
      next_choice=input("Enter your choice: ")
      if next_choice.isdigit() and 0 <= int(next_choice) <= 8:
                break
      else:
                print("Invalid choice. Please enter a number between 0 and 8.")
                continue
     if next_choice=='1':
        pass
     if next_choice=='2':
        pass
     if next_choice=='3':
        pass
     if next_choice=='4':
        clear_screen()
        current_user.show_patrons_info()
        enter=input("Press Enter to return to the menu.")
        clear_screen()
        continue
        
     if next_choice=='5':
        pass
     if next_choice=='6':
        pass
     if next_choice=='7':
        pass
     if next_choice=='8':
         clear_screen()
         current_user=None
         clear_screen()
         login_menu()
         break
    
     if next_choice=='0':
        print("Thank you for using the Library Management System. Goodbye!")
        exit()  
   
    




# Call the function to display the menu




#TENTATIVE PA YUNG MGA NUMBER NG MENU BAKA KASI MAY MADAGDAG
def menu_10_1():#MENU 5.1 ADD PATRON 
    print("Select Patron Type to Add:")
    print("1. Student")
    print("2. Faculty")
    print("3. Community")
    print("4. Child") 
    
def menu6_1():#MENU 6.1 EDIT BOOK STATUS
    print("Select Book Status to Edit:")
    print("1. Available")
    print("2. Checked Out")
    print("3. Reserved")
    print("4. Lost")

    #ILAGAY YUNG CURRENTUSER.ADDPATRON LATER ON
with open('librarian1.csv', mode='r', newline='') as file:
    if os.path.getsize('librarian1.csv') == 0 or len(file.readlines()) <= 1:
        first_menu()
    else:
        login_menu()
print('james')