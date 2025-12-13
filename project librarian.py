import datetime
import os
import random
import csv
import json
import pandas as pd
if not os.path.exists('patron1.csv') or os.path.getsize('patron1.csv') == 0:
    with open('patron1.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        # order: name, age, library_number, fines, days_overdue, max_books_allowed,
        # max_days_allowed, contact_number, book_preferences, borrowed_books, object
        writer.writerow([
            'name', 'age', 'library_number', 'fines',
            'days_overdue', 'max_books_allowed', 'max_days_allowed',
            'contact_number', 'book_preferences', 'borrowed_books', 'object'
        ])
if not os.path.exists('assistant1.csv') or os.path.getsize('assistant1.csv') == 0:
    with open('assistant1.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'age', 'username', 'password', 'library_number', 'object'])
if not os.path.exists('librarian1.csv') or os.path.getsize('librarian1.csv') == 0:
    with open('librarian1.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'age', 'username', 'password', 'library_number', 'object'])
fines_collected=0.0

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
        
        clean_row = {k.strip(): (v.strip() if v and isinstance(v, str) else v) for k, v in row.items() if k}
        
        # gonna skip if missing the fields
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
        num = random.randint(10000, 99999)  # 5digit number
        if num not in used_library_numbers:
            used_library_numbers.add(num)
            return num

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
    def search_book(self):#DONE
             
            import os, csv
            clear_screen()
            print("Search Books")
        
            books_path = 'books123.updated.csv'
            if not os.path.exists(books_path):
                print("Books file not found.")
                input("\nPress Enter to return to menu...")
                return
        
            # menu
            print("Search by:")
            print("1. Book number")
            print("2. Title")
            print("3. ISBN")
            choice = input("Choose an option (1-3) or B to cancel: ").strip().lower()
            if not choice or choice == 'b':
                return
        
            def share_detail_book(b):
                lines = []
                lines.append(f"Book ID: {b.get('bookID','')}")
                lines.append(f"Title: {b.get('title','')}")
                lines.append(f"Authors: {b.get('authors','')}")
                lines.append(f"Average Rating: {b.get('average_rating','')}")
                lines.append(f"ISBN: {b.get('isbn','')}  ISBN13: {b.get('isbn13','')}")
                lines.append(f"Pages: {b.get('num_pages','')}  Language: {b.get('language_code','')}")
                lines.append(f"Ratings: {b.get('ratings_count','')}  Reviews: {b.get('text_reviews_count','')}")
                lines.append(f"Publication Date: {b.get('publication_date','')}  Publisher: {b.get('publisher','')}")
                lines.append(f"Status: {b.get('Status', b.get('status',''))}  Checkouts: {b.get('Checkouts','')} ")
                return '\n'.join(lines)
        
            def show_the_book(b, width_title=48, width_auth=20):
                bid = str(b.get('bookID','')).ljust(6)
                title = (b.get('title','') or '')[:width_title].ljust(width_title)
                authors = (b.get('authors','') or '')[:width_auth].ljust(width_auth)
                isbn = (b.get('isbn','') or '').ljust(13)
                status = (b.get('Status') or b.get('status') or '').ljust(12)
                return f"{bid}  {title}  {authors}  {isbn}  {status}"
        
            # read all rows up-front
            with open(books_path, mode='r', encoding='utf-8', newline='') as bf:
                reader = csv.DictReader(bf)
                rows = list(reader)
        
            if choice == '1':
                # exact book number search
                bid = input("Enter Book ID (exact) or B to cancel: ").strip()
                if not bid or bid.lower() == 'b':
                    return
                match = next((r for r in rows if (r.get('bookID') or '').strip() == bid), None)
                if not match:
                    print(f"No book found with Book ID '{bid}'.")
                    input("\nPress Enter to return to menu...")
                    return
                clear_screen()
                print(share_detail_book(match))
                input("\n\nPress Enter to return to menu...")
                return
        
            # title or isbn => paginated list of 10 with selection
            mapperr = {'2': 'title', '3': 'isbn'}
            field = mapperr.get(choice)
            if not field:
                print("Invalid choice.")
                return
        
            term = input(f"Enter search term for {field} (case-insensitive) or B to cancel: ").strip()
            if not term or term.lower() == 'b':
                return
        
            term_lower = term.lower()
            def matches_term(r):
                return term_lower in (r.get(field) or '').lower()
        
            matched = [r for r in rows if matches_term(r)]
            if not matched:
                print("No matches found.")
                input("\nPress Enter to return to menu...")
                return
        
            # pagination + searcherrigation + selection
            page = 0
            page_size = 10
            total = len(matched)
            while True:
                clear_screen()
                start = page * page_size
                end = min(start + page_size, total)
                page_items = matched[start:end]
        
                # header for summary list (no left-most index; checkouts added at right)
                print(f"Showing results {start+1}-{end} of {total} for '{term}' (field: {field})")
                print("BookID  Title                                             Authors              ISBN          Status       Checkouts")
                print("------  " + "-"*48 + "  " + "-"*20 + "  " + "-"*13 + "  " + "-"*12 + "  " + "-"*9)
                for r in page_items:
                    print(show_the_book(r) + "  " + str(r.get('Checkouts', '')))

                # prompt for searcherrigation or selection by BookID
                print("\nOptions: enter a Book ID to view details, 'N' next, 'P' previous, 'B' back to menu")
                searcherr = input("Choice: ").strip()

                if not searcherr:
                    continue
                loweringg = searcherr.lower()
                if loweringg == 'b':
                    return
                if loweringg == 'n':
                    if end >= total:
                        print("No more pages.")
                        input("\nPress Enter to return to menu...")
                        return
                    page += 1
                    continue
                if loweringg == 'p':
                    if page == 0:
                        print("Already at first page.")
                        input("\nPress Enter to continue...")
                        continue
                    page -= 1
                    continue

                # treat input as BookID selection
                chosen = next((m for m in matched if (m.get('bookID') or '').strip() == searcherr), None)
                if chosen:
                    clear_screen()
                    print(share_detail_book(chosen))
                    input("\n\nPress Enter to return to results...")
                    # keep page where the chosen item appears
                    try:
                        index_selectt = matched.index(chosen)
                        page = index_selectt // page_size
                    except Exception:
                        pass
                    continue

                print("Invalid input or Book ID not in results.")
                input("\nPress Enter to continue...")
                continue

    def change_password(self):
        clear_screen()
        print("Change Password")
        current_password = input("Enter current password: ")
        if current_password != self.password:
            print("Incorrect current password.")
            return
        new_password = input("Enter new password: ")
        confirm_password = input("Confirm new password: ")
        if new_password != confirm_password:
            print("New passwords do not match.")
            return

        path = 'librarian1.csv' if isinstance(self, Librarian) else 'assistant1.csv'
        with open(path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            records = list(reader)

        with open(path, mode='w', newline='') as file:
            fieldnames = ['name', 'age', 'username', 'password', 'library_number', 'object']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for record in records:
                if record['username'] == self.username:
                    record['password'] = new_password
                writer.writerow(record)

        self.password = new_password
        print("Password changed successfully.")

    def add_book(self):#DONE
        clear_screen()
        print("Add a book")
        title = input("Enter book title: ")
        authors = input("Enter book author(s): ")
        isbn = input("Enter book ISBN: ")
        
        # check if  ISBN already exist
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
        s = 'books123.updated.csv'
        if not os.path.exists(s):
            print("Books file not found.")
            return

        book_id = input("Enter Book ID to remove (or B to cancel): ").strip()
        if not book_id or book_id.lower() == 'b':
            print("Aborted.")
            return

        # backup csv
        bak = s + '.bak'
        try:
            shutil.copy2(s, bak)
        except Exception:
            pass

        # read raw CSV
        with open(s, mode='r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            try:
                header = next(reader)
            except StopIteration:
                print("CSV is empty.")
                return
            rows = [row for row in reader]

        column_id = 0
        for i, h in enumerate(header):
            if h and h.strip().lower() == 'bookid':
                column_id = i
                break

        matches = [ (i, r) for i, r in enumerate(rows) if len(r) > column_id and r[column_id].strip() == book_id ]
        if not matches:
            print(f"Book ID '{book_id}' not found.")
            return

        column_title = next((i for i,h in enumerate(header) if h and h.strip().lower() == 'title'), None)
        column_isbn  = next((i for i,h in enumerate(header) if h and h.strip().lower() == 'isbn'), None)
        for indexx, r in matches:
            title = r[column_title] if column_title is not None and column_title < len(r) else ''
            isbn =  r[column_isbn]  if column_isbn  is not None and column_isbn  < len(r) else ''
            print(f"  row_index={indexx}  bookID={r[column_id]}  title={title[:80]}  isbn={isbn}")

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
            os.replace(tmp, s)
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)

        removed_isbns = set()
        for _, r in matches:
            if column_isbn is not None and column_isbn < len(r):
                removed_isbns.add(r[column_isbn].strip())
        global books
        books[:] = [b for b in books if (b.isbn or '').strip() not in removed_isbns]

        print(f"Removed {len(remove_indices)} record(s).")
    def delete_own_account(self):
        clear_screen()
        username = self.username
        confirm = input(f"Are you sure you want to delete your account '{username}'? This action cannot be undone. (y/N): ").strip().lower()
        if confirm != 'y':
            print("Account deletion aborted.")
            return

        path = 'librarian1.csv' if isinstance(self, Librarian) else 'assistant1.csv'
        with open(path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            records = list(reader)

        with open(path, mode='w', newline='') as file:
            fieldnames = ['name', 'age', 'username', 'password', 'library_number', 'object']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            removed = False
            for record in records:
                if record['username'] != username:
                    writer.writerow(record)
                else:
                    removed = True

            if removed:
                print(f'Account with username {username} deleted successfully.')
            else:
                print(f'Account with username {username} not found.')
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
            p_fieldnames = preader.fieldnames or ['name','age','library_number','fines','days_overdue','max_books_allowed','max_days_allowed','contact_number','book_preferences','borrowed_books','object']
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
                p_fieldnames = preader.fieldnames or ['name','age','library_number','fines','days_overdue','max_books_allowed','max_days_allowed','contact_number','book_preferences','borrowed_books','object']
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

            # chosen columns and compute widths (contact and preferences shown before borrowed_books)
            cols = ['name', 'age', 'library_number', 'fines', 'days_overdue', 'max_books_allowed', 'max_days_allowed', 'contact_number', 'book_preferences', 'borrowed_books']
            headers = ['Name', 'Age', 'Library no.', 'Fines', 'Days Overdue', 'Max Books', 'Max Days', 'Contact', 'Preferences', 'Borrowed Books']
            widths = []
            for h, c in zip(headers, cols):
                w = max(len(h), max((len(str(p.get(c, ''))) for p in patrons), default=0))
                widths.append(w)

            # header
            header_line = '  '.join(h.ljust(w) for h, w in zip(headers, widths))
            sep_line = '  '.join('-' * w for w in widths)
            print(header_line)
            print(sep_line)

            # rows
            for p in patrons:
                row = []
                for c, w in zip(cols, widths):
                    row.append(str(p.get(c, '')).ljust(w))
                print('  '.join(row))


class Librarian(Staff):
    def __repr__(self):
        return f'Librarian({self.name}, {self.age}, {self.username})'
    @classmethod
    def add_librarian(cls):#DONE
        clear_screen()
        print('=' * 40)
        print('Welcome to the library management system!')
        print('Since this is your first time, please create a librarian account to get started.')
        print('=' * 40)
        print('')
        name = input("Enter librarian's name: ")
        while True:
            try:
                age = int(input("Enter librarian's age: "))
                if age < 0:
                    print("Age cannot be negative. Please try again.")
                    continue
                break
            except ValueError:
                print("Please enter a valid integer for age.")

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
    

    def add_assistant(self): #DONE
        name = input("Enter assistant's name: ")
        
        while True:
            try:
                age = int(input("Enter assistant's age: "))
                if age < 0:
                    print("Age cannot be negative. Please try again.")
                    continue
                break
            except ValueError:
                print("Please enter a valid integer for age.")
        
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
        
        print(f"Assistant '{username}' has been successfully created.") #DONE
        

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

            # compute column widths
            name_w = max(len('Name'), max((len(str(a.get('name',''))) for a in assistants), default=0))
            age_w = max(len('Age'), max((len(str(a.get('age',''))) for a in assistants), default=0))
            user_w = max(len('Username'), max((len(str(a.get('username',''))) for a in assistants), default=0))

            # header
            print(f"{ 'Name'.ljust(name_w) }  { 'Age'.ljust(age_w) }  { 'Username'.ljust(user_w) }")
            print(f"{ '-'*name_w }  { '-'*age_w }  { '-'*user_w }")

            # rows
            for assistant in assistants:
                print(f"{ str(assistant.get('name','')).ljust(name_w) }  { str(assistant.get('age','')).ljust(age_w) }  { str(assistant.get('username','')).ljust(user_w) }")


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
            # Ensure age is <= 12 for Child; re-prompt safely on invalid input
            while age > 12:
                print("Age exceeds the limit for Child patron type.")
                try:
                    childd = int(input("Enter a valid age (12 or below): ").strip())
                except ValueError:
                    print("Please enter a valid integer for age.")
                    # keep age > 12 so the loop continues
                    age = 13
                    continue
                age = childd
                # loop will continue if childd > 12, otherwise break
            new_patron = Child(name, age, library_number)
            print(f'Child added with library number: {library_number}')
        # ask for contact number and preferences (stored in CSV only)
        contact_number = input("Enter contact number(optional): ").strip()
        book_preferences = input("Enter book preferences:(optional) ").strip()

        with open('patron1.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            # CSV column order: name, age, library_number, fines,
            # days_overdue, max_books_allowed, max_days_allowed,
            # contact_number, book_preferences, borrowed_books, object
            writer.writerow([
                new_patron.name, new_patron.age, new_patron.library_number, new_patron.fines,
                new_patron.days_overdue, new_patron.max_books_allowed, new_patron.max_days_allowed,
                contact_number, book_preferences, new_patron.borrowed_books, repr(new_patron)
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
            fieldnames = ['name', 'age', 'library_number', 'fines',
                          'days_overdue', 'max_books_allowed', 'max_days_allowed',
                          'contact_number', 'book_preferences', 'borrowed_books', 'object']
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
    enter=input("\nPress Enter to continue to the menu.")
    clear_screen()
    librarian_menu()
    
            
            

def login_menu():#LOGIN MENU
    global current_user
    print("Welcome to the Library Management System")
    print("Please log in to continue.")
    print("1. Librarian Login")
    print("2. Assistant Login")
    print("3. Exit\n\n")
    print("NOTE: If you are an assistant and do not have an account yet, please contact the librarian to create one for you.")
    while True:
        choice=input("Enter your choice: ")
        
        if choice in ['1', '2', '3']:
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")
    while True:
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
            print('In case you forgot your password, go back to the VIDEO DEMO to retrieve your account(NOTE:This file is strictly for librarian)')
            enterr=input('\nPress enter to continue\n')
            
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
            print('In case you forgot your username or password, contact your librarian to retrieve your account')
            enterr=input('\nPress enter to continue\n')
            
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
     print("1. Add Book")#RESTY
     print("2. Remove Book")#RESTY
     print('3. Lend Book/Receive Book/Edit book status')#RESTY
     print("4. Show Patron Info")#DONE!
     print('5. Receive fines from Patron')#RESTY
     print("6. Add Assistant")#DONE
     print("7. Show Assistants")#DOne
     print("8. Remove Assistant")#DOne
     print("9. Add Patron")#DOne
     print("10. Remove Patron")#DOne
     print("11. Edit Patron Info")#RESTY
     print('12. Show transaction history')#RESTY
     print("13. Calculate Overall Fines")#RESTY
     print("14. Delete Own Account")#done
     print("15. Generate Report")#RESTY
     print('16. Search Books')#done
     print("17. Logout")#DONE
     print('18. Change password')#done
     print("0. Exit\n")#done
     while True:
        next_choice=input("Enter your choice: ")
        if next_choice.isdigit() and 0 <= int(next_choice) <= 18:
            break
        else:
            print("Invalid choice. Please enter a number between 0 and 18.")
     if next_choice=='1': #RESTY
        clear_screen()
        current_user.add_book()
        enter=input("\nPress Enter to return to the menu.")
        clear_screen()
        continue
     if next_choice=='2':#RESTY
        clear_screen()
        current_user.remove_book()
        enter=input("\nPress Enter to return to the menu.")
        clear_screen()
        continue
     if next_choice=='3':#resty
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
        if choice=='1':#resty
            current_user.lend_book()
            enter=input("\nPress Enter to return to the menu.")
            clear_screen()
            continue
        if choice=='2':#resty
            current_user.receive_book()
            enter=input("\nPress Enter to return to the menu.")
            clear_screen()
            continue
        if choice=='3':#resty
            clear_screen()
            menu6_1()
            current_user.edit_book_status_and_update_patron()
            enter=input("\nPress Enter to return to the menu.")
            clear_screen()
            continue
     if next_choice=='4':#DONE
        clear_screen()
        current_user.show_patrons_info()
        enter=input("\nPress Enter to return to the menu.")
        clear_screen()
        continue
     if next_choice=='5':#resty
        pass
     if next_choice=='6':
        clear_screen()
        current_user.add_assistant()
        enter=input("\nPress Enter to return to the menu.")
        clear_screen()
        continue
     if next_choice=='7':
        clear_screen()
        current_user.show_assistants_info()
        enter=input("\nPress Enter to return to the menu.")
        clear_screen()
        continue
     if next_choice=='8':
        clear_screen()
        current_user.remove_assistant()
        enter=input("\nPress Enter to return to the menu.")
        clear_screen()
        continue

     if next_choice=='9':
        clear_screen()
        menu_10_1()
        current_user.add_patron()
        enter=input("\nPress Enter to return to the menu.")
        clear_screen()
        continue
     if next_choice=='10':
        clear_screen()
        current_user.remove_patron()
        enter=input("\nPress Enter to return to the menu.")
        clear_screen()
        continue
     if next_choice=='11':#resty
        pass
     if next_choice=='12':#restyt
        pass
     if next_choice=='13':#resty
        pass
     if next_choice=='14':
        clear_screen()
        current_user.delete_own_account()
        enter=input("\nPress Enter to return to the menu.")
        clear_screen()
        starting_point()
        break
     
        
     if next_choice=='15':#resty
        pass
     if next_choice=='16':
        clear_screen()
        current_user.search_book()
        clear_screen()
        continue
     if next_choice=='17':
       clear_screen()
       current_user=None
       clear_screen()
       login_menu()
       break

     if next_choice=='18':
        clear_screen()
        current_user.change_password()
        enter=input("\nPress Enter to return to the menu.")
        clear_screen()
        continue
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
     print("1. Add Book")#resty
     print("2. Remove Book")#resty
     print("3. Lend Book/Receive Book/Edit book status")#resty
     print("4. Show Patron Info")#done
     print("5. Receive fines from Patron")#resty
     print("6. Delete Own Account")#done
     print("7. Search Books")#done
     print("8. Logout")#done
     print("0. Exit\n")#done
     while True:
      next_choice=input("Enter your choice: ")
      if next_choice.isdigit() and 0 <= int(next_choice) <= 8:
                break
      else:
                print("Invalid choice. Please enter a number between 0 and 8.")
                continue
     if next_choice=='1':#resty
        pass
     if next_choice=='2':#resty
        pass
     if next_choice=='3':#restyt
        pass
     if next_choice=='4':
        clear_screen()
        current_user.show_patrons_info()
        enter=input("\nPress Enter to return to the menu.")
        clear_screen()
        continue
        
     if next_choice=='5':#resty
        pass
     if next_choice=='6':
        clear_screen()
        current_user.delete_own_account()
        enter=input("\nPress Enter to return to the menu.")
        clear_screen()
        starting_point()
        break
     if next_choice=='7':
        clear_screen()
        current_user.search_book()
        clear_screen()
        continue
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
#START OF CODE
def starting_point():
 with open('librarian1.csv', mode='r', newline='') as file:
    if os.path.getsize('librarian1.csv') == 0 or len(file.readlines()) <= 1:
        first_menu()
    else:
        login_menu()
starting_point()