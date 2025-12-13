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

# --- Transactions helpers: create log file, append, and view ---
import datetime as _dt

def init_transactions(path='transactions.csv'):
    """Create transactions CSV if missing with header."""
    import csv, os
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp','type','actor_username','patron_library_number','bookID','amount','note'])

def log_transaction(t_type, actor_username=None, patron_library_number=None, bookID=None, amount=0.0, note=None, path='transactions.csv'):
    """Append a transaction record to the transactions CSV.

    t_type: short string like 'lend','receive','fine_payment'
    actor_username: librarian/assistant username performing action
    patron_library_number: integer or string
    bookID: book identifier
    amount: numeric amount (fines collected etc.)
    note: optional free-text note
    """
    import csv, os
    init_transactions(path)
    ts = _dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(path, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([ts, t_type, actor_username or '', patron_library_number or '', bookID or '', f"{amount}", note or ''])

def view_transactions(limit=50, path='transactions.csv'):
    """Return last `limit` transactions as list of dicts (most recent first)."""
    import csv, os
    init_transactions(path)
    rows = []
    with open(path, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    # return most recent first
    return rows[-limit:][::-1]

# ensure transactions file exists on startup
init_transactions()

def clear_screen():
   
    if os.name == 'nt':
        os.system('cls')

    else:
     os.system('clear')


current_user = None
current_client = None  # Track the patron who borrowed the book

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
    def calculate_overdue_fines(self):
        """Calculate fines for overdue books by comparing due_date to today's date."""
        import os, csv, json, datetime, tempfile, shutil
        clear_screen()
        print("Calculate Overdue Fines")
        
        patron_path = 'patron1.csv'
        if not os.path.exists(patron_path):
            print("Patron file not found.")
            return
        
        # Read patrons
        with open(patron_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            raw_fieldnames = reader.fieldnames or []
            fieldnames = [fn for fn in raw_fieldnames if fn and str(fn).strip()]
            patrons = list(reader)
        
        today = datetime.date.today()
        fine_per_day = 5.0  # $5 per day late
        total_fines_added = 0.0
        
        print(f"Checking overdue books for {len(patrons)} patron(s)...\n")
        
        for patron in patrons:
            # Parse borrowed_books
            bb_raw = patron.get('borrowed_books', '{}')
            borrowed = {}
            try:
                borrowed = json.loads(bb_raw) if bb_raw else {}
            except Exception:
                borrowed = {}
            
            if not borrowed:
                continue
            
            # Get current fines
            try:
                current_fines = float(patron.get('fines', 0))
            except ValueError:
                current_fines = 0.0
            
            overdue_books = {}
            patron_fines_added = 0.0
            
            # Check each borrowed book for overdue status
            for isbn_key, book_info in borrowed.items():
                if isinstance(book_info, dict):
                    due_date_str = book_info.get('due_date', '')
                    if due_date_str:
                        try:
                            due_date = datetime.date.fromisoformat(due_date_str)
                            if today > due_date:
                                days_overdue = (today - due_date).days
                                fine_amount = days_overdue * fine_per_day
                                
                                # Add to overdue_books
                                overdue_books[isbn_key] = {
                                    'bookID': book_info.get('bookID', ''),
                                    'title': book_info.get('title', 'Unknown'),
                                    'checkout_date': book_info.get('checkout_date', ''),
                                    'due_date': due_date_str,
                                    'days_overdue': days_overdue,
                                    'fine': fine_amount
                                }
                                patron_fines_added += fine_amount
                        except (ValueError, TypeError):
                            continue
            
            # Update patron if any overdue books found
            if overdue_books:
                new_fines = current_fines + patron_fines_added
                patron['fines'] = str(new_fines)
                patron['overdue_books'] = json.dumps(overdue_books)
                
                # Display details
                print(f"Patron: {patron.get('name')} (Library #: {patron.get('library_number')})")
                for isbn_key, book in overdue_books.items():
                    print(f"  📚 {book['title']}")
                    print(f"     Due: {book['due_date']} | Days Late: {book['days_overdue']} | Fine: ${book['fine']:.2f}")
                print(f"  Total Fine Added: ${patron_fines_added:.2f} | New Total: ${new_fines:.2f}\n")
                
                total_fines_added += patron_fines_added
        
        # Write updated patrons back to CSV
        if total_fines_added > 0:
            fd, tmp_path = tempfile.mkstemp(prefix='patrons_', suffix='.csv', dir='.')
            os.close(fd)
            
            with open(tmp_path, mode='w', newline='', encoding='utf-8') as out:
                writer = csv.DictWriter(out, fieldnames=fieldnames)
                writer.writeheader()
                sanitized_patrons = []
                for p in patrons:
                    clean_patron = {fn: (p.get(fn, '') if p.get(fn) is not None else '') for fn in fieldnames}
                    sanitized_patrons.append(clean_patron)
                writer.writerows(sanitized_patrons)
            
            shutil.move(tmp_path, patron_path)
            print(f"✓ Total fines calculated and added: ${total_fines_added:.2f}")
        else:
            print("✓ No overdue books found. All patrons are current on their loans.")
        

            
    def lend_book(self):
        import os, csv, json, datetime, tempfile, shutil

        clear_screen()
        print("Lend a Book")

        # --- Get Patron ---
        lib_input = input("Enter patron library number (or B to cancel): ").strip()
        if not lib_input or lib_input.lower() == 'b':
            return

        try:
            library_number = int(lib_input)
        except ValueError:
            print("Invalid library number.")
            return

        patron_path = 'patron1.csv'
        if not os.path.exists(patron_path):
            print("Patron file not found.")
            return

        with open(patron_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            raw_fieldnames = reader.fieldnames or []
            # Sanitize fieldnames: remove None and empty strings
            fieldnames = [fn for fn in raw_fieldnames if fn and str(fn).strip()]
            patrons = list(reader)

        patron = None
        for p in patrons:
            try:
                if int(p.get('library_number', -1)) == library_number:
                    patron = p
                    break
            except ValueError:
                continue

        if not patron:
            print("Patron not found.")
            return

        # --- Parse borrowed_books safely ---
        borrowed = {}
        raw_borrowed = patron.get('borrowed_books', '{}')

        try:
            borrowed = json.loads(raw_borrowed) if raw_borrowed else {}
        except Exception:
            borrowed = {}

        # --- Check borrowing limit ---
        try:
            max_books = int(patron.get('max_books_allowed', 0))
        except ValueError:
            max_books = 0

        if max_books and len(borrowed) >= max_books:
            print(f"Patron already reached max borrowed books ({max_books}).")
            return

        # --- Get Book ---
        book_id = input("Enter Book ID to lend (or B to cancel): ").strip()
        if not book_id or book_id.lower() == 'b':
            return

        books_path = 'books123.updated.csv'
        if not os.path.exists(books_path):
            print("Books file not found.")
            return

        with open(books_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            book_fields = reader.fieldnames
            books_rows = list(reader)

        book = None
        for b in books_rows:
            if b.get('bookID') == book_id:
                book = b
                break

        if not book:
            print("Book not found.")
            return

        if book.get('Status', '').lower() == 'checked out':
            print("Book is already checked out.")
            return

        # --- Update book status ---
        book['Status'] = 'Checked Out'
        try:
            book['Checkouts'] = str(int(book.get('Checkouts', 0)) + 1)
        except ValueError:
            book['Checkouts'] = '1'

        # --- Write updated books file ---
        fd, tmp = tempfile.mkstemp()
        os.close(fd)

        with open(tmp, mode='w', newline='', encoding='utf-8') as out:
            writer = csv.DictWriter(out, fieldnames=book_fields)
            writer.writeheader()
            writer.writerows(books_rows)

        shutil.move(tmp, books_path)

        # --- Compute dates ---
        today = datetime.date.today()

        try:
            max_days = int(patron.get('max_days_allowed', 0))
        except (ValueError, TypeError):
            max_days = 0

        due_date = (today + datetime.timedelta(days=max_days)).isoformat() if max_days else ""

        isbn_key = book.get('isbn') or book.get('isbn13') or book_id

        borrowed[isbn_key] = {
            "bookID": book_id,
            "title": book.get("title", ""),
            "checkout_date": today.isoformat(),
            "due_date": due_date,
            "isbn": book.get("isbn", "")
        }

        patron['borrowed_books'] = json.dumps(borrowed)

        # --- Write updated patron file (sanitize fieldnames) ---
        fd2, tmp2 = tempfile.mkstemp()
        os.close(fd2)

        with open(tmp2, mode='w', newline='', encoding='utf-8') as out:
            writer = csv.DictWriter(out, fieldnames=fieldnames)
            writer.writeheader()
            # Sanitize each patron row to only include valid fieldnames
            sanitized_patrons = []
            for p in patrons:
                clean_patron = {fn: (p.get(fn, '') if p.get(fn) is not None else '') for fn in fieldnames}
                sanitized_patrons.append(clean_patron)
            writer.writerows(sanitized_patrons)

        shutil.move(tmp2, patron_path)

        # --- Success message ---
        print("\n✓ Book successfully lent!")
        print(f"Patron : {patron.get('name')}")
        print(f"Book   : {book.get('title')}")
        print(f"Date   : {today.isoformat()}")
        print(f"Due    : {due_date if due_date else 'No limit'}")
        # Log transaction
        try:
            log_transaction('lend', actor_username=getattr(self, 'username', ''), patron_library_number=library_number, bookID=book_id, amount=0.0, note=f"Lent '{book.get('title','')}'")
        except Exception:
            pass

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
        # Log receive transaction
        try:
            log_transaction('receive', actor_username=getattr(self, 'username', ''), patron_library_number='', bookID=book_id, amount=0.0, note=f"Received return of bookID {book_id}")
        except Exception:
            pass
    def edit_book_status(self):
        import tempfile, os, csv, shutil
        clear_screen()
        print("Edit Book Status")
        
        book_id = input("Enter Book ID to edit (or B to cancel): ").strip()
        if not book_id or book_id.lower() == 'b':
            print("Aborted.")
            return

        books_path = 'books123.updated.csv'
        if not os.path.exists(books_path):
            print("Books file not found.")
            return

        # Read books
        with open(books_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            raw_fieldnames = reader.fieldnames or []
            fieldnames = [fn for fn in raw_fieldnames if fn and str(fn).strip()]
            books_rows = list(reader)

        # Find book
        book = None
        for row in books_rows:
            if (row.get('bookID') or '').strip() == book_id:
                book = row
                break

        if not book:
            print(f"Book ID {book_id} not found.")
            return

        # Show current status
        current_status = (book.get('Status') or '').strip()
        print(f"\nCurrent Book Details:")
        print(f"  Title: {book.get('title', '')}")
        print(f"  Current Status: {current_status}")
        print(f"  Checkouts: {book.get('Checkouts', '0')}")

        # Show status options
        print("\nSelect New Status:")
        print("1. Available")
        print("2. Checked Out")
        print("3. Reserved")
        print("4. Lost")

        choice = input("Enter your choice (1-4) or B to cancel: ").strip()
        if choice.lower() == 'b':
            print("Aborted.")
            return

        status_map = {
            '1': 'Available',
            '2': 'Checked Out',
            '3': 'Reserved',
            '4': 'Lost'
        }

        if choice not in status_map:
            print("Invalid choice.")
            return

        new_status = status_map[choice]

        # Update status
        book['Status'] = new_status

        # Write updated books file
        fd, tmp_path = tempfile.mkstemp(prefix='books_', suffix='.csv', dir='.')
        os.close(fd)

        with open(tmp_path, mode='w', newline='', encoding='utf-8') as out:
            writer = csv.DictWriter(out, fieldnames=fieldnames)
            writer.writeheader()
            sanitized_rows = []
            for row in books_rows:
                clean_row = {fn: (row.get(fn, '') if row.get(fn) is not None else '') for fn in fieldnames}
                sanitized_rows.append(clean_row)
            writer.writerows(sanitized_rows)

        shutil.move(tmp_path, books_path)

        print(f"\n✓ Book ID {book_id} status updated from '{current_status}' to '{new_status}'.")
    
    def receive_fines_from_patron(self):
        import os, csv, datetime, tempfile, shutil
        clear_screen()
        print("Receive Fines from Patron")
        
        lib_input = input("Enter patron library number (or B to cancel): ").strip()
        if not lib_input or lib_input.lower() == 'b':
            print("Aborted.")
            return
        
        try:
            library_number = int(lib_input)
        except ValueError:
            print("Invalid library number.")
            return
        
        patron_path = 'patron1.csv'
        if not os.path.exists(patron_path):
            print("Patron file not found.")
            return
        
        # Read patrons
        with open(patron_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            raw_fieldnames = reader.fieldnames or []
            fieldnames = [fn for fn in raw_fieldnames if fn and str(fn).strip()]
            patrons = list(reader)
        
        # Find patron
        patron = None
        for p in patrons:
            try:
                if int(p.get('library_number', -1)) == library_number:
                    patron = p
                    break
            except ValueError:
                continue
        
        if not patron:
            print(f"Patron with library number {library_number} not found.")
            return
        
        # Show patron info and current fines only (do not auto-calc or display overdue-book fines here)
        try:
            current_fines = float(patron.get('fines', 0))
        except Exception:
            current_fines = 0.0
        # capture existing overdue entries so we can act on them after payment
        raw_overdue = patron.get('overdue_books', '{}')
        try:
            overdue_entries = json.loads(raw_overdue) if raw_overdue else {}
        except Exception:
            overdue_entries = {}
        
        print(f"\nPatron Information:")
        print(f"  Name: {patron.get('name', '')}")
        print(f"  Library Number: {library_number}")
        print(f"  Current Fines: ${current_fines:.2f}")
        print("\n(Overdue book computation is handled in the transaction menu.)")
        
        if current_fines <= 0:
            print("\n  Patron has no outstanding fines.")
            return
        
        # Get payment amount
        while True:
            try:
                payment = float(input(f"\nEnter payment amount (max ${current_fines:.2f}): ").strip())
                if payment < 0:
                    print("Payment amount cannot be negative.")
                    continue
                if payment > current_fines:
                    print(f"Payment exceeds outstanding fines (${current_fines:.2f}).")
                    continue
                break
            except ValueError:
                print("Invalid amount. Please enter a valid number.")
        
        if payment == 0:
            print("No payment received.")
            return
        
        # Update fines
        new_fines = current_fines - payment
        patron['fines'] = str(new_fines)
        # If fully paid, clear overdue bookkeeping so it isn't shown as unpaid
        try:
            if float(new_fines) <= 0:
                # clear overdue_books and reset days_overdue
                patron['overdue_books'] = '{}'
                patron['days_overdue'] = '0'
                # Also remove these overdue items from patron.borrowed_books and mark books Available
                # Update borrowed_books JSON for this patron
                try:
                    bb_raw = patron.get('borrowed_books', '{}') or '{}'
                    borrowed = json.loads(bb_raw) if isinstance(bb_raw, str) and bb_raw else (bb_raw if isinstance(bb_raw, dict) else {})
                except Exception:
                    borrowed = {}

                # remove overdue keys from borrowed
                for k in list(overdue_entries.keys()):
                    if k in borrowed:
                        del borrowed[k]
                try:
                    patron['borrowed_books'] = json.dumps(borrowed)
                except Exception:
                    patron['borrowed_books'] = '{}'

                # mark affected books as Available in books CSV
                try:
                    books_path = 'books123.updated.csv'
                    if os.path.exists(books_path):
                        with open(books_path, mode='r', encoding='utf-8', newline='') as bfile:
                            reader = csv.DictReader(bfile)
                            raw_b_fieldnames = reader.fieldnames or []
                            b_fieldnames = [fn for fn in raw_b_fieldnames if fn and str(fn).strip()]
                            books_rows = list(reader)

                        changed = False
                        for entry_key, info in overdue_entries.items():
                            isbn_key = str(entry_key)
                            bookid = (info.get('bookID') or '').strip() if isinstance(info, dict) else ''
                            for row in books_rows:
                                if (row.get('bookID') or '').strip() == bookid or (row.get('isbn') or '').strip() == isbn_key:
                                    row['Status'] = 'Available'
                                    changed = True

                        if changed:
                            fd3, tmp3 = tempfile.mkstemp(prefix='books_', suffix='.csv', dir='.')
                            os.close(fd3)
                            try:
                                with open(tmp3, mode='w', encoding='utf-8', newline='') as out:
                                    writer = csv.DictWriter(out, fieldnames=b_fieldnames)
                                    writer.writeheader()
                                    # sanitize rows
                                    sanitized = [{fn: (r.get(fn, '') if r.get(fn) is not None else '') for fn in b_fieldnames} for r in books_rows]
                                    writer.writerows(sanitized)
                                shutil.move(tmp3, books_path)
                            finally:
                                if os.path.exists(tmp3):
                                    try: os.remove(tmp3)
                                    except Exception: pass
                except Exception:
                    pass
        except Exception:
            pass
        
        # Write patrons back to CSV (sanitize rows)
        fd, tmp_path = tempfile.mkstemp(prefix='patrons_', suffix='.csv', dir='.')
        os.close(fd)
        try:
            with open(tmp_path, mode='w', newline='', encoding='utf-8') as out:
                writer = csv.DictWriter(out, fieldnames=fieldnames)
                writer.writeheader()
                sanitized_patrons = []
                for p in patrons:
                    clean_patron = {fn: (p.get(fn, '') if p.get(fn) is not None else '') for fn in fieldnames}
                    sanitized_patrons.append(clean_patron)
                writer.writerows(sanitized_patrons)
            shutil.move(tmp_path, patron_path)
        finally:
            if os.path.exists(tmp_path):
                try: os.remove(tmp_path)
                except Exception: pass
        
        # Update global fines_collected
        global fines_collected
        fines_collected += payment
        
        # Success message
        print(f"\n✓ Payment received: ${payment:.2f}")
        print(f"  Remaining fines: ${new_fines:.2f}")
        print(f"  Total fines collected today: ${fines_collected:.2f}")
        # Log fine payment
        try:
            log_transaction('fine_payment', actor_username=getattr(self, 'username', ''), patron_library_number=library_number, bookID='', amount=payment, note=f"Payment of ${payment:.2f}")
        except Exception:
            pass
    def report(self):
        """Generate reports: books, patrons, transactions, or fines."""
        while True:
            clear_screen()
            print("===== Reports Menu =====\n")
            print("1. Books Report")
            print("2. Patrons Report")
            print("3. Transactions Report")
            print("4. Fines Report")
            print("0. Back to Menu\n")
            choice = input("Enter your choice (0-4): ").strip()

            if choice == '1':
                self._report_books()
            elif choice == '2':
                self._report_patrons()
            elif choice == '3':
                self._report_transactions()
            elif choice == '4':
                self._report_fines()
            elif choice == '0':
                return
            else:
                print("Invalid choice.")
                input("\nPress Enter to continue...")

    def _report_books(self):
        """Display all books in inventory."""
        clear_screen()
        print("===== Books Report =====\n")
        try:
            with open('books123.updated.csv', mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                if not rows:
                    print("No books found.")
                    input("\nPress Enter to return...")
                    return

                total = len(rows)
                available = sum(1 for r in rows if (r.get('Status') or '').lower() == 'available')
                checked_out = sum(1 for r in rows if (r.get('Status') or '').lower() == 'checked out')

                print(f"Total Books: {total}")
                print(f"Available: {available}")
                print(f"Checked Out: {checked_out}\n")

                print("BookID    | Title                                      | ISBN         | Status       | Checkouts")
                print("---------+--------------------------------------------+--------------+--------------+----------")
                for r in rows[:50]:  # show first 50
                    bid = (r.get('bookID') or '')[:8].ljust(8)
                    title = (r.get('title') or '')[:42].ljust(42)
                    isbn = (r.get('isbn') or '')[:12].ljust(12)
                    status = (r.get('Status') or '')[:12].ljust(12)
                    checkouts = (r.get('Checkouts') or '0')
                    print(f"{bid} | {title} | {isbn} | {status} | {checkouts}")
                if len(rows) > 50:
                    print(f"\n... and {len(rows) - 50} more books")

        except Exception as e:
            print(f"Error reading books: {e}")
        input("\nPress Enter to return...")

    def _report_patrons(self):
        """Display all patrons and their status."""
        clear_screen()
        print("===== Patrons Report =====\n")
        try:
            with open('patron1.csv', mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                if not rows:
                    print("No patrons found.")
                    input("\nPress Enter to return...")
                    return

                total = len(rows)
                with_fines = sum(1 for r in rows if float(r.get('fines', 0) or 0) > 0)
                total_fines = sum(float(r.get('fines', 0) or 0) for r in rows)

                print(f"Total Patrons: {total}")
                print(f"Patrons with Fines: {with_fines}")
                print(f"Total Fines Outstanding: ${total_fines:.2f}\n")

                print("Name                    | Library#  | Fines        | Borrowed | Days Overdue")
                print("------------------------+-----------+--------------+----------+-----------")
                for r in rows:
                    name = (r.get('name') or '')[:24].ljust(24)
                    lib = (r.get('library_number') or '')[:9].ljust(9)
                    fines = f"${float(r.get('fines', 0) or 0):.2f}".ljust(12)
                    borrowed = (r.get('borrowed_books') or '')
                    try:
                        b_count = len(json.loads(borrowed) if borrowed else {})
                    except:
                        b_count = 0
                    borrowed_str = str(b_count).ljust(8)
                    days_overdue = (r.get('days_overdue') or '0')
                    print(f"{name} | {lib} | {fines} | {borrowed_str} | {days_overdue}")

        except Exception as e:
            print(f"Error reading patrons: {e}")
        input("\nPress Enter to return...")

    def _report_transactions(self):
        """Display transaction summary."""
        clear_screen()
        print("===== Transactions Report =====\n")
        try:
            recent = view_transactions(100)
            if not recent:
                print("No transactions found.")
                input("\nPress Enter to return...")
                return

            # count by type
            lend_count = sum(1 for t in recent if t.get('type') == 'lend')
            receive_count = sum(1 for t in recent if t.get('type') == 'receive')
            payment_count = sum(1 for t in recent if t.get('type') == 'fine_payment')
            total_paid = sum(float(t.get('amount', 0) or 0) for t in recent if t.get('type') == 'fine_payment')

            print(f"Total Transactions: {len(recent)}")
            print(f"Books Lent: {lend_count}")
            print(f"Books Received: {receive_count}")
            print(f"Fine Payments: {payment_count}")
            print(f"Total Fines Collected: ${total_paid:.2f}\n")

            # build patron lookup
            patron_map = {}
            try:
                with open('patron1.csv', mode='r', newline='', encoding='utf-8') as pfile:
                    preader = csv.DictReader(pfile)
                    for pr in preader:
                        key = (pr.get('library_number') or '').strip()
                        if key:
                            patron_map[key] = pr.get('name', '').strip()
            except Exception:
                pass

            print("Date       | Type             | Patron                | Amount")
            print("-----------+------------------+-----------------------+---------")
            for t in recent[-20:]:  # last 20
                ts_raw = t.get('timestamp', '')
                ts = ''
                if ts_raw:
                    try:
                        ts = _dt.datetime.fromisoformat(ts_raw).date().isoformat()
                    except:
                        ts = ts_raw[:10]
                ttype = (t.get('type', '') or '')[:16].ljust(16)
                patron_key = (t.get('patron_library_number', '') or '').strip()
                if patron_key and patron_key in patron_map:
                    patron_display = f"{patron_map[patron_key]}({patron_key})"[:21].ljust(21)
                else:
                    patron_display = (patron_key or '')[:21].ljust(21)
                amount = t.get('amount', '') or ''
                print(f"{ts} | {ttype} | {patron_display} | {amount}")

        except Exception as e:
            print(f"Error reading transactions: {e}")
        input("\nPress Enter to return...")

    def _report_fines(self):
        """Display patrons with outstanding fines."""
        clear_screen()
        print("===== Fines Report =====\n")
        try:
            with open('patron1.csv', mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                fines_rows = [r for r in rows if float(r.get('fines', 0) or 0) > 0]

                if not fines_rows:
                    print("No patrons with outstanding fines.")
                    input("\nPress Enter to return...")
                    return

                total_fines = sum(float(r.get('fines', 0) or 0) for r in fines_rows)

                print(f"Patrons with Outstanding Fines: {len(fines_rows)}")
                print(f"Total Fines: ${total_fines:.2f}\n")

                print("Name                    | Library#  | Fines        | Days Overdue")
                print("------------------------+-----------+--------------+----------")
                for r in sorted(fines_rows, key=lambda x: float(x.get('fines', 0) or 0), reverse=True):
                    name = (r.get('name') or '')[:24].ljust(24)
                    lib = (r.get('library_number') or '')[:9].ljust(9)
                    fines = f"${float(r.get('fines', 0) or 0):.2f}".ljust(12)
                    days_overdue = (r.get('days_overdue') or '0')
                    print(f"{name} | {lib} | {fines} | {days_overdue}")

        except Exception as e:
            print(f"Error reading fines: {e}")
        input("\nPress Enter to return...")
    def view_transactions(self):
        """Show recent transactions (most recent first)."""
        clear_screen()
        print("Recent Transactions")
        try:
            recent = view_transactions(100)
        except Exception:
            print("Could not read transactions file.")
            return
        if not recent:
            print("No transactions recorded yet.")
            return
        # build patron lookup from patron1.csv -> library_number -> name
        patron_map = {}
        try:
            with open('patron1.csv', mode='r', newline='', encoding='utf-8') as pfile:
                preader = csv.DictReader(pfile)
                for pr in preader:
                    key = (pr.get('library_number') or '').strip()
                    if key:
                        patron_map[key] = pr.get('name', '').strip()
        except Exception:
            patron_map = {}

        # pretty print using patron info when available as a table
        cols = [
            ('timestamp', 10),    # YYYY-MM-DD
            ('type', 12),
            ('actor', 12),
            ('patron', 24),
            ('bookID', 8),
            ('amount', 10),
            ('note', 40),
        ]

        rows = []
        for t in recent:
            ts_raw = t.get('timestamp','')
            ts = ''
            if ts_raw:
                try:
                    ts = _dt.datetime.fromisoformat(ts_raw).date().isoformat()
                except Exception:
                    ts = ts_raw[:10]

            ttype = (t.get('type','') or '')
            actor = (t.get('actor_username','') or '')
            patron_key = (t.get('patron_library_number','') or '').strip()
            if patron_key and patron_key in patron_map:
                patron_display = f"{patron_map[patron_key]}({patron_key})"
            else:
                patron_display = patron_key or ''
            bookid = (t.get('bookID','') or '')
            amount = (t.get('amount','') or '')
            note = (t.get('note','') or '')
            rows.append((ts, ttype, actor, patron_display, bookid, amount, note))

        # compute column widths (respect max widths)
        widths = []
        for i, (name, maxw) in enumerate(cols):
            header_len = len(name)
            content_max = max((len(str(r[i])) for r in rows), default=0)
            w = min(max(header_len, content_max), maxw)
            widths.append(w)

        # header
        header = ' | '.join(name.ljust(widths[i]) for i, (name, _) in enumerate(cols))
        sep = '-+-'.join('-' * widths[i] for i in range(len(cols)))
        print(header)
        print(sep)

        # rows (truncate note if necessary)
        for r in rows:
            out = []
            for i, cell in enumerate(r):
                s = str(cell)
                w = widths[i]
                if len(s) > w:
                    s = s[:max(0, w-3)] + '...'
                out.append(s.ljust(w))
            print(' | '.join(out))
        input("\nPress Enter to return to menu...")
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

    def edit_patron_info(self):
        """Edit patron information: name, age, contact, preferences, borrowing limits."""
        import tempfile, shutil
        clear_screen()
        print("Edit Patron Information")

        lib_input = input("Enter patron library number (or B to cancel): ").strip()
        if not lib_input or lib_input.lower() == 'b':
            print("Aborted.")
            return

        try:
            library_number = int(lib_input)
        except ValueError:
            print("Invalid library number.")
            return

        patron_path = 'patron1.csv'
        if not os.path.exists(patron_path):
            print("Patron file not found.")
            return

        # Read patrons
        with open(patron_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            raw_fieldnames = reader.fieldnames or []
            fieldnames = [fn for fn in raw_fieldnames if fn and str(fn).strip()]
            patrons = list(reader)

        # Find patron
        patron = None
        for p in patrons:
            try:
                if int(p.get('library_number', -1)) == library_number:
                    patron = p
                    break
            except ValueError:
                continue

        if not patron:
            print(f"Patron with library number {library_number} not found.")
            return

        # Show current info
        clear_screen()
        print(f"Patron: {patron.get('name', '')}")
        print(f"Library Number: {library_number}\n")
        print("Current Information:")
        print(f"  Age: {patron.get('age', '')}")
        print(f"  Contact: {patron.get('contact_number', '')}")
        print(f"  Preferences: {patron.get('book_preferences', '')}")
        print(f"  Max Books: {patron.get('max_books_allowed', '')}")
        print(f"  Max Days: {patron.get('max_days_allowed', '')}\n")

        # Edit menu
        while True:
            print("Edit Options:")
            print("1. Name")
            print("2. Age")
            print("3. Contact Number")
            print("4. Book Preferences")
            print("5. Max Books Allowed")
            print("6. Max Days Allowed")
            print("0. Done\n")

            choice = input("Enter your choice (0-6): ").strip()

            if choice == '0':
                break
            elif choice == '1':
                new_name = input("Enter new name: ").strip()
                if new_name:
                    patron['name'] = new_name
                    print("✓ Name updated.")
            elif choice == '2':
                try:
                    new_age = int(input("Enter new age: ").strip())
                    if new_age >= 0:
                        patron['age'] = str(new_age)
                        print("✓ Age updated.")
                    else:
                        print("Age cannot be negative.")
                except ValueError:
                    print("Invalid age.")
            elif choice == '3':
                new_contact = input("Enter new contact number: ").strip()
                patron['contact_number'] = new_contact
                print("✓ Contact updated.")
            elif choice == '4':
                new_prefs = input("Enter new book preferences: ").strip()
                patron['book_preferences'] = new_prefs
                print("✓ Preferences updated.")
            elif choice == '5':
                try:
                    new_max = int(input("Enter new max books allowed: ").strip())
                    if new_max >= 0:
                        patron['max_books_allowed'] = str(new_max)
                        print("✓ Max books updated.")
                    else:
                        print("Max books cannot be negative.")
                except ValueError:
                    print("Invalid number.")
            elif choice == '6':
                try:
                    new_days = int(input("Enter new max days allowed: ").strip())
                    if new_days >= 0:
                        patron['max_days_allowed'] = str(new_days)
                        print("✓ Max days updated.")
                    else:
                        print("Max days cannot be negative.")
                except ValueError:
                    print("Invalid number.")
            else:
                print("Invalid choice.")
            print()

        # Write patrons back to CSV (sanitize rows)
        fd, tmp_path = tempfile.mkstemp(prefix='patrons_', suffix='.csv', dir='.')
        os.close(fd)
        try:
            with open(tmp_path, mode='w', newline='', encoding='utf-8') as out:
                writer = csv.DictWriter(out, fieldnames=fieldnames)
                writer.writeheader()
                sanitized_patrons = []
                for p in patrons:
                    clean_patron = {fn: (p.get(fn, '') if p.get(fn) is not None else '') for fn in fieldnames}
                    sanitized_patrons.append(clean_patron)
                writer.writerows(sanitized_patrons)
            shutil.move(tmp_path, patron_path)
            print(f"✓ Patron information updated successfully.")
        finally:
            if os.path.exists(tmp_path):
                try: os.remove(tmp_path)
                except Exception: pass
        input("\nPress Enter to return to the menu...")


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
     print("1. Add Book")#DONE
     print("2. Remove Book")#DONE
     print('3. Lend Book/Receive Book/Edit book status')#DONE
     print("4. Show Patron Info")#DONE
     print('5. Receive fines from Patron')#DONE
     print("6. Add Assistant")#DONE
     print("7. Show Assistants")#DOne
     print("8. Remove Assistant")#DOne
     print("9. Add Patron")#DOne
     print("10. Remove Patron")#DOne
     print("11. Edit Patron Info")#done
     print('12. Show transaction history')#Done
     print("13. Calculate Overall Fines")#Done
     print("14. Delete Own Account")#done
     print("15. Generate Report")#Done
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
            current_user.edit_book_status()
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
        clear_screen()
        current_user.receive_fines_from_patron()
        enter=input("\nPress Enter to return to the menu.")
        clear_screen()
        continue
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
        current_user.edit_patron_info()
        enter=input("\nPress Enter to return to the menu.")
        clear_screen()
        continue
     if next_choice=='12':#restyt
        clear_screen()
        try:
            current_user.view_transactions()
        except Exception:
            print("Could not load transactions.")
        enter=input("\nPress Enter to return to the menu.")
        clear_screen()
        continue
     if next_choice=='13':#resty
        clear_screen()
        current_user.calculate_overdue_fines()
        enter=input("\nPress Enter to return to the menu.")
        clear_screen()
        continue
     if next_choice=='14':
        clear_screen()
        current_user.delete_own_account()
        enter=input("\nPress Enter to return to the menu.")
        clear_screen()
        starting_point()
        break
     
        
     if next_choice=='15':#resty
        clear_screen()
        current_user.report()
        enter=input("\nPress Enter to return to the menu.")
        clear_screen()
        continue
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
            current_user.edit_book_status()
            enter=input("\nPress Enter to return to the menu.")
            clear_screen()
            continue
     if next_choice=='4':
        clear_screen()
        current_user.show_patrons_info()
        enter=input("\nPress Enter to return to the menu.")
        clear_screen()
        continue
     if next_choice=='5':#resty
        clear_screen()
        current_user.receive_fines_from_patron()
        enter=input("\nPress Enter to return to the menu.")
        clear_screen()
        continue
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