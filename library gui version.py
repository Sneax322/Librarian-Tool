# =====================================================
# IMPORTS & SETUP
# =====================================================
import sys
import subprocess
import csv
import os
import json
import datetime
import uuid
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

try:
    import customtkinter as ctk
except ImportError:
    print("Installing customtkinter...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
    import customtkinter as ctk

# =====================================================
# THEME & CONSTANTS
# =====================================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


FONT_HEADER = ("Segoe UI", 24, "bold")
FONT_BOLD = ("Segoe UI", 18, "bold")

TREE_FONT_ROW = ("Segoe UI", 18)
TREE_FONT_HEAD = ("Segoe UI", 18, "bold")
TREE_ROW_HEIGHT = 40

BG_DARK = "#1e1e1e"
BG_CARD = "#2a2a2a"
BG_TABLE = "#262626"
FG_TEXT = "#ffffff"
ACCENT_BLUE = "#1f6aa5"
ACCENT_RED = "#a83232"
ACCENT_GREEN = "#2d8a44"

# =====================================================
# PATHS
# =====================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
BOOKS_PATH = os.path.join(SCRIPT_DIR, "books123.updated.csv")
PATRONS_PATH = os.path.join(SCRIPT_DIR, "patron1.csv")
LIBRARIANS_PATH = os.path.join(SCRIPT_DIR, "librarian1.csv")
ASSISTANTS_PATH = os.path.join(SCRIPT_DIR, "assistant1.csv")
TRANSACTIONS_PATH = os.path.join(SCRIPT_DIR, "transactions.csv")

# =====================================================
# BUSINESS LOGIC MODELS
# =====================================================
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Patron(Person):
    def __init__(self, name, age, library_number, max_books=5, max_days=30):
        super().__init__(name, age)
        self.library_number = library_number
        self.max_books = max_books
        self.max_days = max_days

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.age})"

class Student(Patron):
    def __init__(self, name, age, lib_num):
        super().__init__(name, age, lib_num, max_books=5, max_days=30)

class Faculty(Patron):
    def __init__(self, name, age, lib_num):
        super().__init__(name, age, lib_num, max_books=10, max_days=60)

class Community(Patron):
    def __init__(self, name, age, lib_num):
        super().__init__(name, age, lib_num, max_books=3, max_days=20)

class Child(Patron):
    def __init__(self, name, age, lib_num):
        super().__init__(name, age, lib_num, max_books=2, max_days=15)

# =====================================================
# DATA HANDLER
# =====================================================
class DataHandler:
    @staticmethod
    def init_files():
        headers_map = {
            BOOKS_PATH: ["bookID","title","authors","average_rating","isbn","isbn13",
                         "language_code","num_pages","ratings_count","text_reviews_count",
                         "publication_date","publisher","Status","Checkouts"],
            PATRONS_PATH: ["name","age","library_number","fines","days_overdue",
                           "max_books_allowed","max_days_allowed","contact_number",
                           "book_preferences","borrowed_books","object"],
            LIBRARIANS_PATH: ["name","age","username","password","library_number","object"],
            ASSISTANTS_PATH: ["name","age","username","password","library_number","object"],
            TRANSACTIONS_PATH: ["timestamp","type","actor_username","patron_library_number","bookID","amount","note"]
        }
        for path, headers in headers_map.items():
            if not os.path.exists(path) or os.path.getsize(path) == 0:
                with open(path, "w", newline="", encoding="utf-8") as f:
                    csv.writer(f).writerow(headers)

    @staticmethod
    def read_csv(path):
        if not os.path.exists(path): return []
        with open(path, "r", newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    @staticmethod
    def write_csv(path, data, headers=None):
        if not data and not headers: return
        if not headers and data: headers = list(data[0].keys())
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)

    @staticmethod
    def log_transaction(t_type, actor, patron_id, book_id, amount, note):
        ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row = {
            "timestamp": ts, "type": t_type, "actor_username": actor,
            "patron_library_number": patron_id, "bookID": book_id,
            "amount": amount, "note": note
        }
        file_exists = os.path.exists(TRANSACTIONS_PATH)
        with open(TRANSACTIONS_PATH, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            if not file_exists: writer.writeheader()
            writer.writerow(row)

# =====================================================
# HELPERS
# =====================================================
def update_all_fines():
    patrons = DataHandler.read_csv(PATRONS_PATH)
    fine_per_day = 5.0
    today = datetime.date.today()
    for p in patrons:
        borrowed = json.loads(p.get("borrowed_books", "{}"))
        overdue_days_count = 0
        current_fine_balance = float(p.get("fines") or 0)
        for isbn, info in borrowed.items():
            due_str = info.get("due_date")
            if due_str:
                try:
                    due_date = datetime.date.fromisoformat(due_str)
                    if today > due_date:
                        days = (today - due_date).days
                        overdue_days_count += days
                except ValueError: pass
        p['days_overdue'] = str(overdue_days_count)
        calculated_fine = overdue_days_count * fine_per_day
        if calculated_fine > current_fine_balance:
            p['fines'] = str(calculated_fine)
    DataHandler.write_csv(PATRONS_PATH, patrons, list(patrons[0].keys()) if patrons else None)

# =====================================================
# GUI CLASSES
# =====================================================

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller
        frame = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(frame, text="Library System Login", font=FONT_HEADER).pack(pady=20, padx=40)
        self.user_entry = ctk.CTkEntry(frame, placeholder_text="Username", width=250)
        self.user_entry.pack(pady=10)
        self.pass_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="*", width=250)
        self.pass_entry.pack(pady=10)
        self.role_var = tk.StringVar(value="Librarian")
        role_frame = ctk.CTkFrame(frame, fg_color="transparent")
        role_frame.pack(pady=10)
        ctk.CTkRadioButton(role_frame, text="Librarian", variable=self.role_var, value="Librarian").pack(side="left", padx=10)
        ctk.CTkRadioButton(role_frame, text="Assistant", variable=self.role_var, value="Assistant").pack(side="left", padx=10)
        ctk.CTkButton(frame, text="Login", command=self.login, width=250).pack(pady=20)
        ctk.CTkButton(frame, text="First Time? Create Librarian", fg_color="transparent", border_width=1, command=lambda: controller.show_frame(RegisterFrame)).pack(pady=(0, 20))

    def login(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()
        role = self.role_var.get()
        path = LIBRARIANS_PATH if role == "Librarian" else ASSISTANTS_PATH
        users = DataHandler.read_csv(path)
        user = next((u for u in users if u['username'] == username and u['password'] == password), None)
        if user: self.controller.login(user, role)
        else: messagebox.showerror("Error", "Invalid credentials")

class RegisterFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller
        frame = ctk.CTkFrame(self, fg_color=BG_CARD)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(frame, text="Register Librarian", font=FONT_HEADER).pack(pady=20)
        self.entries = {}
        for field in ["Name", "Age", "Username", "Password"]:
            ctk.CTkEntry(frame, placeholder_text=field, width=250).pack(pady=5)
            self.entries[field] = frame.winfo_children()[-1]
        ctk.CTkButton(frame, text="Register", command=self.register).pack(pady=20)
        ctk.CTkButton(frame, text="Back", fg_color="transparent", command=lambda: controller.show_frame(LoginFrame)).pack()

    def register(self):
        data = {k: v.get() for k, v in self.entries.items()}
        if not all(data.values()): return
        try: int(data['Age'])
        except ValueError:
            messagebox.showerror("Error", "Age must be a number")
            return
        existing = DataHandler.read_csv(LIBRARIANS_PATH)
        if any(u['username'] == data['Username'] for u in existing):
            messagebox.showerror("Error", "Username taken")
            return
        row = {"name": data['Name'], "age": data['Age'], "username": data['Username'], "password": data['Password'], "library_number": str(uuid.uuid4())[:8], "object": f"Librarian({data['Name']}, {data['Age']})"}
        with open(LIBRARIANS_PATH, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            if os.path.getsize(LIBRARIANS_PATH) == 0: writer.writeheader()
            writer.writerow(row)
        messagebox.showinfo("Success", "Account created")
        self.controller.show_frame(LoginFrame)

class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller
        
        # Navbar
        nav = ctk.CTkFrame(self, height=50, corner_radius=0)
        nav.pack(fill="x")
        self.welcome_lbl = ctk.CTkLabel(nav, text="Welcome", font=FONT_BOLD)
        self.welcome_lbl.pack(side="left", padx=20)
        ctk.CTkButton(nav, text="Logout", width=80, fg_color=ACCENT_RED, command=controller.logout).pack(side="right", padx=10, pady=10)
        ctk.CTkButton(nav, text="Settings", width=80, command=self.open_settings).pack(side="right", padx=0, pady=10)

        # Main Layout
        self.container = ctk.CTkFrame(self, fg_color=BG_DARK)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # Tabs
        self.tabview = ctk.CTkTabview(self.container)
        self.tabview.pack(fill="both", expand=True)
        self.tab_books = self.tabview.add("Books")
        self.tab_patrons = self.tabview.add("Patrons")
        self.tab_reports = self.tabview.add("Reports & Fines")
        self.tab_staff = self.tabview.add("Staff")

        self.init_books_tab()
        self.init_patrons_tab()
        self.init_reports_tab()
        self.init_staff_tab()

    def update_user_info(self):
        u = self.controller.current_user
        role = self.controller.role
        self.welcome_lbl.configure(text=f"User: {u['name']} ({role})")
        if role != "Librarian":
            try: self.tabview.delete("Staff")
            except: pass

    def open_settings(self):
        win = ctk.CTkToplevel(self)
        win.title("User Settings")
        win.geometry("300x250")
        ctk.CTkLabel(win, text="Change Password", font=FONT_BOLD).pack(pady=10)
        new_pass = ctk.CTkEntry(win, placeholder_text="New Password", show="*")
        new_pass.pack(pady=5)
        def save_pass():
            if not new_pass.get(): return
            role = self.controller.role
            path = LIBRARIANS_PATH if role == "Librarian" else ASSISTANTS_PATH
            users = DataHandler.read_csv(path)
            for u in users:
                if u['username'] == self.controller.current_user['username']:
                    u['password'] = new_pass.get()
            DataHandler.write_csv(path, users)
            messagebox.showinfo("Success", "Password Updated")
            win.destroy()
        ctk.CTkButton(win, text="Update", command=save_pass).pack(pady=10)
        ctk.CTkLabel(win, text="Danger Zone", text_color=ACCENT_RED, font=FONT_BOLD).pack(pady=(20,5))
        def delete_account():
            if not messagebox.askyesno("Confirm", "Are you sure? This cannot be undone."): return
            role = self.controller.role
            path = LIBRARIANS_PATH if role == "Librarian" else ASSISTANTS_PATH
            users = DataHandler.read_csv(path)
            new_users = [u for u in users if u['username'] != self.controller.current_user['username']]
            DataHandler.write_csv(path, new_users)
            win.destroy()
            self.controller.logout()
        ctk.CTkButton(win, text="Delete Account", fg_color=ACCENT_RED, command=delete_account).pack()

    # ==========================
    # BOOKS TAB
    # ==========================
    def init_books_tab(self):
        tool_fr = ctk.CTkFrame(self.tab_books, fg_color="transparent")
        tool_fr.pack(fill="x", pady=5)
        ctk.CTkButton(tool_fr, text="+ Add Book", command=self.add_book_dialog).pack(side="left", padx=5)
        ctk.CTkButton(tool_fr, text="Change Status", command=self.change_book_status_dialog).pack(side="left", padx=5) # <--- ADDED BUTTON
        ctk.CTkButton(tool_fr, text="Remove Book", fg_color=ACCENT_RED, command=self.remove_book).pack(side="left", padx=5)
        self.book_search = ctk.CTkEntry(tool_fr, placeholder_text="Search Title/ISBN")
        self.book_search.pack(side="right", padx=5)
        ctk.CTkButton(tool_fr, text="Search", width=60, command=self.refresh_books).pack(side="right")
        
        cols = ("ID", "Title", "Author", "ISBN", "Status", "Checkouts")
        self.book_tree = ttk.Treeview(self.tab_books, columns=cols, show="headings", height=15)
        for c in cols: self.book_tree.heading(c, text=c)
        self.book_tree.column("ID", width=80)
        self.book_tree.column("Title", width=300)
        self.book_tree.pack(fill="both", expand=True)

    def refresh_books(self):
        for i in self.book_tree.get_children(): self.book_tree.delete(i)
        books = DataHandler.read_csv(BOOKS_PATH)
        query = self.book_search.get().lower()
        for b in books:
            if query in b.get('title','').lower() or query in b.get('isbn',''):
                self.book_tree.insert("", "end", values=(b.get('bookID'), b.get('title'), b.get('authors'), b.get('isbn'), b.get('Status', 'Available'), b.get('Checkouts', 0)))

    def change_book_status_dialog(self): # <--- ADDED METHOD
        sel = self.book_tree.selection()
        if not sel: 
            messagebox.showwarning("Select", "Select a book first to change its status.")
            return
        
        item_values = self.book_tree.item(sel[0])['values']
        book_id = str(item_values[0])
        current_title = item_values[1]
        current_status = item_values[4]

        win = ctk.CTkToplevel(self)
        win.title(f"Change Status: {book_id}")
        win.geometry("350x250")

        ctk.CTkLabel(win, text=f"Book: {current_title}", font=FONT_BOLD).pack(pady=10)
        ctk.CTkLabel(win, text=f"Current Status: {current_status}").pack(pady=(0, 5))
        
        status_var = ctk.StringVar(value=current_status)
        # Statuses from the original logic
        statuses = ["Available", "Checked Out", "Reserved", "Lost", "Damaged"]
        ctk.CTkOptionMenu(win, variable=status_var, values=statuses).pack(pady=10)

        def save():
            new_status = status_var.get()
            books = DataHandler.read_csv(BOOKS_PATH)
            
            found = False
            for book in books:
                if str(book.get('bookID')) == book_id:
                    book['Status'] = new_status
                    found = True
                    break
            
            if found:
                DataHandler.write_csv(BOOKS_PATH, books)
                messagebox.showinfo("Success", f"Status of Book ID {book_id} updated to {new_status}")
                DataHandler.log_transaction("status_change", self.controller.current_user['username'], "", book_id, 0, f"Status manually set to {new_status}")
                win.destroy()
                self.refresh_books() # Refresh book list
            else:
                messagebox.showerror("Error", "Book ID not found in data.")

        ctk.CTkButton(win, text="Update Status", command=save).pack(pady=20)


    def add_book_dialog(self):
        win = ctk.CTkToplevel(self)
        win.title("Add Book")
        win.geometry("400x500")
        fields = ["Title", "Authors", "ISBN", "Publisher", "Year", "Pages"]
        entries = {}
        for f in fields:
            ctk.CTkEntry(win, placeholder_text=f).pack(pady=5, padx=20, fill="x")
            entries[f] = win.winfo_children()[-1]
        def save():
            books = DataHandler.read_csv(BOOKS_PATH)
            max_id = max([int(b['bookID']) for b in books if b['bookID'].isdigit()] or [0])
            new_book = {
                "bookID": str(max_id + 1), "title": entries["Title"].get(), "authors": entries["Authors"].get(),
                "isbn": entries["ISBN"].get(), "publisher": entries["Publisher"].get(), "publication_date": entries["Year"].get(),
                "num_pages": entries["Pages"].get(), "Status": "Available", "Checkouts": 0
            }
            if not new_book['title']: return
            # Ensure all required columns are present when writing back
            headers = DataHandler.read_csv(BOOKS_PATH)[0].keys() if DataHandler.read_csv(BOOKS_PATH) else ["bookID","title","authors","average_rating","isbn","isbn13","language_code","num_pages","ratings_count","text_reviews_count","publication_date","publisher","Status","Checkouts"]
            
            # Fill missing keys with empty strings to match headers
            for h in headers:
                if h not in new_book:
                    new_book[h] = ''

            books.append(new_book)
            DataHandler.write_csv(BOOKS_PATH, books, headers)
            win.destroy()
            self.refresh_books()

    def remove_book(self):
        sel = self.book_tree.selection()
        if not sel: return
        book_id = str(self.book_tree.item(sel[0])['values'][0])
        if messagebox.askyesno("Confirm", "Delete this book?"):
            books = DataHandler.read_csv(BOOKS_PATH)
            books = [b for b in books if str(b['bookID']) != book_id]
            DataHandler.write_csv(BOOKS_PATH, books)
            self.refresh_books()

    # ==========================
    # PATRONS TAB
    # ==========================
    def init_patrons_tab(self):
        tool_fr = ctk.CTkFrame(self.tab_patrons, fg_color="transparent")
        tool_fr.pack(fill="x", pady=5)
        ctk.CTkButton(tool_fr, text="Register Patron", command=self.add_patron_dialog).pack(side="left", padx=5)
        ctk.CTkButton(tool_fr, text="Lend Book", command=self.lend_book_dialog).pack(side="left", padx=5)
        ctk.CTkButton(tool_fr, text="Return Book", fg_color=ACCENT_GREEN, command=self.return_book_dialog).pack(side="left", padx=5)
        ctk.CTkButton(tool_fr, text="Remove", fg_color=ACCENT_RED, command=self.remove_patron).pack(side="right", padx=5)
        
        # RESTORED COLUMNS: Name, Library #, Age, Type, Fines, Borrowed Details
        cols = ("Name", "Library #", "Age", "Type", "Fines", "Borrowed")
        self.patron_tree = ttk.Treeview(self.tab_patrons, columns=cols, show="headings", height=15)
        for c in cols: self.patron_tree.heading(c, text=c)
        self.patron_tree.column("Name", width=150)
        self.patron_tree.column("Library #", width=80)
        self.patron_tree.column("Age", width=50)
        self.patron_tree.column("Type", width=80)
        self.patron_tree.column("Fines", width=80)
        self.patron_tree.column("Borrowed", width=400) # Wide column for details
        self.patron_tree.pack(fill="both", expand=True)

    def refresh_patrons(self):
        for i in self.patron_tree.get_children(): self.patron_tree.delete(i)
        patrons = DataHandler.read_csv(PATRONS_PATH)
        for p in patrons:
            p_type = p.get('object', '').split('(')[0]
            
            # FORMAT BORROWED BOOKS: "ID: Title" instead of count
            borrowed_data = json.loads(p.get('borrowed_books', '{}'))
            
            # We need to map book IDs to titles to display full details in borrowed_str
            # Re-fetch the book titles here or rely on the data stored in the patron's borrowed_books json
            
            if borrowed_data:
                # The data structure for borrowed books might not contain the title/id, so we'll look it up
                book_details = []
                all_books = DataHandler.read_csv(BOOKS_PATH)
                book_map = {b['bookID']: b['title'] for b in all_books}
                
                for book_id in borrowed_data.keys():
                    title = book_map.get(book_id, 'Unknown Title')
                    book_details.append(f"{book_id}: {title}")
                borrowed_str = ", ".join(book_details)
            else:
                borrowed_str = ""

            self.patron_tree.insert("", "end", values=(
                p.get('name'), 
                p.get('library_number'),
                p.get('age'),
                p_type, 
                f"${float(p.get('fines', 0)):.2f}", 
                borrowed_str
            ))

    def add_patron_dialog(self):
        win = ctk.CTkToplevel(self)
        win.title("Register Patron")
        win.geometry("300x400")
        name_ent = ctk.CTkEntry(win, placeholder_text="Name")
        name_ent.pack(pady=5)
        age_ent = ctk.CTkEntry(win, placeholder_text="Age")
        age_ent.pack(pady=5)
        type_var = ctk.StringVar(value="Student")
        ctk.CTkOptionMenu(win, variable=type_var, values=["Student", "Faculty", "Community", "Child"]).pack(pady=5)
        def save():
            try:
                age = int(age_ent.get())
                if type_var.get() == "Child" and age > 12:
                    messagebox.showerror("Error", "Child must be <= 12")
                    return
            except ValueError: return
            name = name_ent.get()
            lib_num = str(uuid.uuid4())[:5]
            cls_map = {"Student": Student, "Faculty": Faculty, "Community": Community, "Child": Child}
            patron_obj = cls_map[type_var.get()](name, age, lib_num)
            row = {"name": name, "age": age, "library_number": lib_num, "fines": 0.0, "days_overdue": 0,
                   "max_books_allowed": patron_obj.max_books, "max_days_allowed": patron_obj.max_days, "borrowed_books": "{}", "object": repr(patron_obj),
                   "contact_number": "", "book_preferences": "" # Include missing fields
                   }
            
            patron_data = DataHandler.read_csv(PATRONS_PATH)
            headers = patron_data[0].keys() if patron_data else row.keys()
            
            with open(PATRONS_PATH, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writerow(row)
            win.destroy()
            self.refresh_patrons()
        ctk.CTkButton(win, text="Save", command=save).pack(pady=20)

    def lend_book_dialog(self):
        sel = self.patron_tree.selection()
        if not sel: 
            messagebox.showwarning("Select", "Select a patron first")
            return
        # Library # is at index 1
        lib_num = self.patron_tree.item(sel[0])['values'][1]
        
        patrons = DataHandler.read_csv(PATRONS_PATH)
        patron = next((p for p in patrons if str(p['library_number']) == str(lib_num)), None)
        
        borrowed = json.loads(patron.get('borrowed_books', '{}'))
        max_b = int(patron.get('max_books_allowed', 5))
        if len(borrowed) >= max_b:
            messagebox.showerror("Limit", "Patron reached borrow limit")
            return
            
        book_id = simpledialog.askstring("Lend", "Enter Book ID:")
        if not book_id: return
        
        books = DataHandler.read_csv(BOOKS_PATH)
        book = next((b for b in books if str(b['bookID']) == book_id), None)
        
        if not book or book.get('Status') != 'Available':
            messagebox.showerror("Error", "Book not found or unavailable")
            return
            
        today = datetime.date.today()
        due = today + datetime.timedelta(days=int(patron.get('max_days_allowed', 30)))
        
        # Only store minimal info (for backwards compatibility), the title lookup is done in refresh_patrons
        borrowed[book_id] = {"due_date": due.isoformat()} 
        
        patron['borrowed_books'] = json.dumps(borrowed)
        book['Status'] = 'Checked Out'
        book['Checkouts'] = int(book.get('Checkouts', 0)) + 1
        
        DataHandler.write_csv(PATRONS_PATH, patrons)
        DataHandler.write_csv(BOOKS_PATH, books)
        DataHandler.log_transaction("lend", self.controller.current_user['username'], lib_num, book_id, 0, f"Due: {due.isoformat()}")
        messagebox.showinfo("Success", "Book Lent")
        self.refresh_patrons()
        self.refresh_books()

    def return_book_dialog(self):
        book_id = simpledialog.askstring("Return", "Enter Book ID:")
        if not book_id: return
        patrons = DataHandler.read_csv(PATRONS_PATH)
        found = False
        for p in patrons:
            borrowed = json.loads(p.get('borrowed_books', '{}'))
            if book_id in borrowed:
                del borrowed[book_id]
                p['borrowed_books'] = json.dumps(borrowed)
                found = True
                books = DataHandler.read_csv(BOOKS_PATH)
                for b in books:
                    if str(b['bookID']) == book_id:
                        b['Status'] = 'Available'
                DataHandler.write_csv(BOOKS_PATH, books)
                DataHandler.log_transaction("return", self.controller.current_user['username'], p['library_number'], book_id, 0, "")
                break
        if found:
            DataHandler.write_csv(PATRONS_PATH, patrons)
            messagebox.showinfo("Success", "Book Returned")
            self.refresh_patrons()
            self.refresh_books()
        else:
            messagebox.showerror("Error", "Book not currently borrowed")

    def remove_patron(self):
        sel = self.patron_tree.selection()
        if not sel: return
        lib_num = str(self.patron_tree.item(sel[0])['values'][1])
        patrons = DataHandler.read_csv(PATRONS_PATH)
        patrons = [p for p in patrons if str(p['library_number']) != lib_num]
        DataHandler.write_csv(PATRONS_PATH, patrons)
        self.refresh_patrons()

    # ==========================
    # REPORTS TAB
    # ==========================
    def init_reports_tab(self):
        update_all_fines()
        fr = ctk.CTkFrame(self.tab_reports, fg_color="transparent")
        fr.pack(fill="x", pady=10)
        ctk.CTkButton(fr, text="Pay Fines", command=self.pay_fines_dialog).pack(side="left", padx=10)
        ctk.CTkButton(fr, text="Generate Full Report", command=self.show_full_report).pack(side="right", padx=10)
        
        ctk.CTkLabel(self.tab_reports, text="Outstanding Fines", font=FONT_BOLD).pack(anchor="w", padx=10)
        cols = ("Name", "ID", "Amount Owed", "Days Overdue")
        self.fine_tree = ttk.Treeview(self.tab_reports, columns=cols, show="headings", height=8)
        for c in cols: self.fine_tree.heading(c, text=c)
        self.fine_tree.pack(fill="x", padx=10)

        ctk.CTkLabel(self.tab_reports, text="Recent Transactions", font=FONT_BOLD).pack(anchor="w", padx=10, pady=(10,0))
        # RESTORED COLUMNS: Time, Type, Actor, Patron, BookID, Amount, Note
        t_cols = ("Time", "Type", "Actor", "Patron", "BookID", "Amount", "Note")
        self.trans_tree = ttk.Treeview(self.tab_reports, columns=t_cols, show="headings", height=8)
        for c in t_cols: self.trans_tree.heading(c, text=c)
        self.trans_tree.column("Time", width=140)
        self.trans_tree.column("Type", width=80)
        self.trans_tree.column("Actor", width=100)
        self.trans_tree.column("Patron", width=100)
        self.trans_tree.column("BookID", width=80)
        self.trans_tree.column("Amount", width=80)
        self.trans_tree.column("Note", width=200)
        self.trans_tree.pack(fill="x", padx=10)

    def refresh_reports(self):
        update_all_fines()
        for i in self.fine_tree.get_children(): self.fine_tree.delete(i)
        patrons = DataHandler.read_csv(PATRONS_PATH)
        for p in patrons:
            try:
                fines = float(p.get('fines', 0))
                if fines > 0:
                    self.fine_tree.insert("", "end", values=(p['name'], p['library_number'], f"${fines:.2f}", p.get('days_overdue', 0)))
            except: continue
        
        for i in self.trans_tree.get_children(): self.trans_tree.delete(i)
        trans = DataHandler.read_csv(TRANSACTIONS_PATH)
        for t in reversed(trans[-50:]):
            self.trans_tree.insert("", "end", values=(
                t.get('timestamp'), 
                t.get('type'), 
                t.get('actor_username'),
                t.get('patron_library_number'),
                t.get('bookID'),
                t.get('amount'),
                t.get('note')
            ))

    def pay_fines_dialog(self):
        sel = self.fine_tree.selection()
        if not sel: return
        item = self.fine_tree.item(sel[0])['values']
        lib_num = str(item[1])
        current_owed = float(str(item[2]).replace('$',''))
        amount = simpledialog.askfloat("Pay", f"Owed: ${current_owed}\nEnter Amount:")
        if not amount or amount <= 0: return
        if amount > current_owed:
            messagebox.showerror("Error", "Cannot overpay")
            return
        patrons = DataHandler.read_csv(PATRONS_PATH)
        for p in patrons:
            if str(p['library_number']) == lib_num:
                new_bal = current_owed - amount
                p['fines'] = f"{new_bal:.2f}"
                DataHandler.log_transaction("fine_pay", self.controller.current_user['username'], lib_num, "", amount, "Fine Payment")
                break
        DataHandler.write_csv(PATRONS_PATH, patrons)
        self.refresh_reports()

    def show_full_report(self):
        books = DataHandler.read_csv(BOOKS_PATH)
        patrons = DataHandler.read_csv(PATRONS_PATH)
        total_books = len(books)
        checked_out = sum(1 for b in books if b.get('Status') == 'Checked Out')
        total_fines = sum(float(p.get('fines', 0)) for p in patrons)
        report_text = (f"=== LIBRARY REPORT ===\nDate: {datetime.date.today()}\n\n-- INVENTORY --\nTotal Books: {total_books}\nChecked Out: {checked_out}\nAvailable: {total_books - checked_out}\n\n-- FINANCE --\nOutstanding Fines: ${total_fines:.2f}\n")
        win = ctk.CTkToplevel(self)
        win.title("Report")
        win.geometry("400x400")
        ctk.CTkTextbox(win, width=380, height=380).pack(pady=10)
        box = win.winfo_children()[0]
        box.insert("0.0", report_text)
        box.configure(state="disabled")

    # ==========================
    # STAFF TAB
    # ==========================
    def init_staff_tab(self):
        tool_fr = ctk.CTkFrame(self.tab_staff, fg_color="transparent")
        tool_fr.pack(fill="x", pady=5)
        ctk.CTkButton(tool_fr, text="Add Assistant", command=self.add_staff_dialog).pack(side="left", padx=5)
        ctk.CTkButton(tool_fr, text="Remove", fg_color=ACCENT_RED, command=self.remove_staff).pack(side="left", padx=5)
        cols = ("Name", "Username", "Age")
        self.staff_tree = ttk.Treeview(self.tab_staff, columns=cols, show="headings")
        for c in cols: self.staff_tree.heading(c, text=c)
        self.staff_tree.pack(fill="both", expand=True)

    def refresh_staff(self):
        for i in self.staff_tree.get_children(): self.staff_tree.delete(i)
        staff = DataHandler.read_csv(ASSISTANTS_PATH)
        for s in staff:
            self.staff_tree.insert("", "end", values=(s['name'], s['username'], s['age']))

    def add_staff_dialog(self):
        win = ctk.CTkToplevel(self)
        win.title("Add Assistant")
        win.geometry("300x350")
        entries = {}
        for f in ["Name", "Age", "Username", "Password"]:
            ctk.CTkEntry(win, placeholder_text=f).pack(pady=5)
            entries[f] = win.winfo_children()[-1]
        def save():
            row = {k.lower(): v.get() for k, v in entries.items()}
            if not all(row.values()): return
            row['library_number'] = str(uuid.uuid4())[:8]
            row['object'] = f"Assistant({row['name']}, {row['age']})"
            
            staff_data = DataHandler.read_csv(ASSISTANTS_PATH)
            headers = staff_data[0].keys() if staff_data else row.keys()
            
            with open(ASSISTANTS_PATH, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writerow(row)
            win.destroy()
            self.refresh_staff()
        ctk.CTkButton(win, text="Create", command=save).pack(pady=20)

    def remove_staff(self):
        sel = self.staff_tree.selection()
        if not sel: return
        user = self.staff_tree.item(sel[0])['values'][1]
        staff = DataHandler.read_csv(ASSISTANTS_PATH)
        staff = [s for s in staff if s['username'] != str(user)]
        DataHandler.write_csv(ASSISTANTS_PATH, staff)
        self.refresh_staff()

# =====================================================
# MAIN APPLICATION CONTROLLER
# =====================================================
class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System 3.0")
        self.geometry("1000x700")
        DataHandler.init_files()
        
        # --- DARK TABLE STYLE CONFIGURATION ---
        self.init_styles()
        
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        self.current_user = None
        self.role = None
        if os.path.getsize(LIBRARIANS_PATH) == 0: self.show_frame(RegisterFrame)
        else: self.show_frame(LoginFrame)

    def init_styles(self):
        """Configures the dark theme for standard Tkinter Treeviews"""
        style = ttk.Style()
        style.theme_use("clam") # 'Clam' allows better color customization

        # Treeview (The rows)
        style.configure("Treeview",
                        background=BG_TABLE,
                        foreground=FG_TEXT,
                        fieldbackground=BG_TABLE,
                        font=TREE_FONT_ROW,      # Larger Font
                        rowheight=TREE_ROW_HEIGHT, # Taller Rows
                        borderwidth=0)
        
        # Headings (The columns)
        style.configure("Treeview.Heading",
                        background="#333333",
                        foreground=FG_TEXT,
                        font=TREE_FONT_HEAD,     # Bold Headers
                        relief="flat")
        
        # Hover/Select Colors
        style.map("Treeview",
                  background=[("selected", ACCENT_BLUE)],
                  foreground=[("selected", "white")])
        
        style.map("Treeview.Heading",
                  background=[("active", ACCENT_BLUE)])

    def show_frame(self, frame_class):
        for widget in self.container.winfo_children(): widget.destroy()
        frame = frame_class(self.container, self)
        frame.pack(fill="both", expand=True)

    def login(self, user, role):
        self.current_user = user
        self.role = role
        self.show_frame(Dashboard)
        dash = self.container.winfo_children()[0]
        dash.update_user_info()
        dash.refresh_books()
        dash.refresh_patrons()
        dash.refresh_reports()
        if role == "Librarian": dash.refresh_staff()

    def logout(self):
        self.current_user = None
        self.role = None
        self.show_frame(LoginFrame)

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()