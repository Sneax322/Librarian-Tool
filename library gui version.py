# =====================================================
# IMPORTS
# =====================================================
import sys
import subprocess

try:
    import customtkinter as ctk
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
    import customtkinter as ctk

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv, os, json, datetime, uuid

# =====================================================
# THEME
# =====================================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

FONT_TITLE = ("Segoe UI", 24, "bold")
FONT_LABEL = ("Segoe UI", 14)
FONT_INPUT = ("Segoe UI", 15)
FONT_BUTTON = ("Segoe UI", 14, "bold")

FONT_SIDEBAR = ("Segoe UI", 15, "bold")
FONT_SEARCH = ("Segoe UI", 15)

FONT_RADIO = ("Segoe UI", 18)

FONT_ENTRY = ("Segoe UI", 15)
ENTRY_WIDTH = 280

TABLE_FONT = ("Segoe UI", 18)
TABLE_HEADER_FONT = ("Segoe UI", 14, "bold")

ENTRY_WIDTH = 280
BG_DARK = "#1e1e1e"
BG_CARD = "#2a2a2a"
BG_TABLE = "#262626"
FG_TEXT = "#ffffff"
ACCENT = "#1f6aa5"


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

os.makedirs(DATA_DIR, exist_ok=True)

# =====================================================
# DATA HANDLER
# =====================================================
class DataHandler:

    @staticmethod
    def generate_id():
        return str(uuid.uuid4())[:8]

    @staticmethod
    def init_csv(path, headers):
        if not os.path.exists(path):
            with open(path, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(headers)

    @staticmethod
    def read_csv(path):
        if not os.path.exists(path):
            return []
        with open(path, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    @staticmethod
    def write_csv(path, data, headers):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, headers)
            writer.writeheader()
            writer.writerows(data)

    @staticmethod
    def authenticate(username, password, role):
        path = LIBRARIANS_PATH if role == "Librarian" else ASSISTANTS_PATH
        for u in DataHandler.read_csv(path):
            if u["username"] == username and u["password"] == password:
                return u
        return None

    @staticmethod
    def log_transaction(t_type, actor, patron, book, amount, note):
        DataHandler.init_csv(
            TRANSACTIONS_PATH,
            ["Time","Type","Actor","Patron","Book","Amount","Note"]
        )
        with open(TRANSACTIONS_PATH, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                t_type, actor, patron, book, amount, note
            ])



# =====================================================
# INIT FILES
# =====================================================
DataHandler.init_csv(
    BOOKS_PATH,
    ["bookID","title","authors","average_rating","isbn","isbn13",
     "language_code","num_pages","ratings_count","text_reviews_count",
     "publication_date","publisher","Status","Checkouts"]
)

DataHandler.init_csv(
    PATRONS_PATH,
    ["name","age","library_number","fines","days_overdue",
     "max_books_allowed","max_days_allowed","contact_number",
     "book_preferences","borrowed_books","object"]
)

DataHandler.init_csv(
    LIBRARIANS_PATH,
    ["name","age","username","password","library_number","object"]
)

DataHandler.init_csv(
    ASSISTANTS_PATH,
    ["name","age","username","password","library_number","object"]
)



# =====================================================
# AUTH SCREENS
# =====================================================
class RegisterLibrarianFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller

        card = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=20)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            card, text="Create Librarian Account",
            font=("Segoe UI", 22, "bold")
        ).pack(pady=20)

        self.entries = {}
        for field in ["Name", "Age", "Username", "Password"]:
            ctk.CTkLabel(card, text=field).pack(anchor="w", padx=40)
            e = ctk.CTkEntry(card, show="*" if field == "Password" else "")
            e.pack(padx=40, pady=5, fill="x")
            self.entries[field] = e

        ctk.CTkButton(
            card, text="Create Account",
            command=self.submit
        ).pack(pady=20, padx=40, fill="x")

    def submit(self):
        data = {k: v.get() for k, v in self.entries.items()}
        if not all(data.values()):
            messagebox.showerror("Error", "All fields required")
            return

        try:
            age = int(data["Age"])
            if age < 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Invalid age")
            return

        with open(LIBRARIANS_PATH, "a", newline="") as f:
            csv.writer(f).writerow([
                data["Name"], age,
                data["Username"], data["Password"],
                DataHandler.generate_id(), "Librarian"
            ])

        messagebox.showinfo("Success", "Librarian created")
        self.controller.switch_frame(LoginFrame)


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller

        card = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=20)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            card, text="Library Login",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=25)

        self.user = ctk.CTkEntry(card, placeholder_text="Username")
        self.user.pack(padx=40, pady=10, fill="x")

        self.pwd = ctk.CTkEntry(card, placeholder_text="Password", show="*")
        self.pwd.pack(padx=40, pady=10, fill="x")

        self.role = tk.StringVar(value="Librarian")
        role_frame = tk.Frame(card, bg=BG_CARD)
        role_frame.pack(pady=10)

        for r in ["Librarian", "Assistant"]:
            tk.Radiobutton(
                role_frame,
                text=r,
                font=FONT_RADIO,
                variable=self.role,
                value=r,
                bg=BG_CARD,
                fg=FG_TEXT,
                activebackground=BG_CARD,
                activeforeground=FG_TEXT,
                selectcolor=BG_TABLE
            ).pack(side="left", padx=12)


        ctk.CTkButton(
            card, text="LOGIN",
            command=self.login
        ).pack(pady=20, padx=40, fill="x")

    def login(self):
        user = DataHandler.authenticate(
            self.user.get(),
            self.pwd.get(),
            self.role.get()
        )
        if user:
            self.controller.login_success(user, self.role.get())
        else:
            messagebox.showerror("Failed", "Invalid credentials")


# =====================================================
# DASHBOARD
# =====================================================
class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller

        # Top bar
        top = tk.Frame(self, bg=BG_CARD, height=50)
        top.pack(fill="x")

        tk.Label(
            top,
            text=f"Logged in as: {controller.current_user['name']} ({controller.user_role})",
            font=("Segoe UI", 24, "bold"),
            bg=BG_CARD,
            fg=FG_TEXT
        ).pack(side="left", padx=20)


        # Sidebar
        sidebar = tk.Frame(self, bg=BG_TABLE, width=200)
        sidebar.pack(side="left", fill="y")

        buttons = [
            ("Books Management", self.show_books),
            ("Patrons & Lending", self.show_patrons),
            ("Reports & Fines", self.show_reports),
        ]

        if controller.user_role == "Librarian":
            buttons.append(("Staff Management", self.show_staff))

        for text, cmd in buttons:
            tk.Button(
                sidebar,
                text=text,
                font=FONT_SIDEBAR,
                bg=BG_TABLE,
                fg=FG_TEXT,
                relief="flat",
                anchor="w",
                padx=14,
                pady=10,
                command=cmd
            ).pack(fill="x", padx=10, pady=6)


        self.content = tk.Frame(self, bg=BG_DARK)
        self.content.pack(fill="both", expand=True, padx=20, pady=20)

        self.show_books()

    def clear(self):
        for w in self.content.winfo_children():
            w.destroy()

    # =====================================================
    # PLACEHOLDERS — IMPLEMENTED NEXT
    # =====================================================
    def show_books(self):
        self.clear()
        BooksManagement(self.content, self.controller).pack(fill="both", expand=True)

    def show_patrons(self):
        self.clear()
        PatronsManagement(self.content, self.controller).pack(fill="both", expand=True)

    def show_reports(self):
        self.clear()
        ReportsManagement(self.content, self.controller).pack(fill="both", expand=True)

    def show_staff(self):
        self.clear()
        StaffManagement(self.content, self.controller).pack(fill="both", expand=True)

# =====================================================
# BOOKS MANAGEMENT
# =====================================================
class BooksManagement(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller

        tk.Label(
            self, text="Books Management",
            font=("Segoe UI", 18, "bold"),
            bg=BG_DARK, fg=FG_TEXT
        ).pack(anchor="w", pady=10)

        controls = tk.Frame(self, bg=BG_DARK)
        controls.pack(fill="x", pady=5)

        ctk.CTkButton(
            controls, text="+ Add Book",
            command=self.add_book).pack(side="left", padx=5)

        ctk.CTkButton(
            controls, text="Remove Selected",
            fg_color="#a83232",
            command=self.remove_book
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            controls, text="Edit Status",
            fg_color="#c47a2c",
            command=self.edit_status
        ).pack(side="left", padx=5)

        tk.Label(
            controls, text="Search:",
            bg=BG_DARK, fg=FG_TEXT
        ).pack(side="left", padx=(30, 5))

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_books)
        self.search_entry = ctk.CTkEntry(
        controls,
        width=260,
        height=36,
        font=FONT_ENTRY,
        placeholder_text="Search..."
    )
        self.search_entry.pack(side="left", padx=6)

        self.search_entry.bind(
            "<KeyRelease>",
            lambda e: self.search_var.set(self.search_entry.get())
        )


        # ---------------- TABLE ----------------
        table_frame = tk.Frame(self, bg=BG_TABLE)
        table_frame.pack(fill="both", expand=True, pady=10)

        style = ttk.Style()
        style.theme_use("default")
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview",
            background=BG_TABLE,
            foreground=FG_TEXT,
            fieldbackground=BG_TABLE,
            font=TABLE_FONT,
            rowheight=34
        )

        style.configure(
            "Treeview.Heading",
            font=TABLE_HEADER_FONT
        )

        style.map(
            "Treeview",
            background=[("selected", ACCENT)]
        )
        style.map("Treeview", background=[("selected", ACCENT)])

        cols = ("ID", "Title", "Author", "ISBN", "Status", "Checkouts")
        self.tree = ttk.Treeview(
            table_frame, columns=cols,
            show="headings", height=20
        )

        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="w")

        self.tree.column("Title", width=280)
        self.tree.pack(fill="both", expand=True)

        self.all_books = DataHandler.read_csv(BOOKS_PATH)
        self.refresh(self.all_books)

    # -------------------------------------------------
    def refresh(self, books):
        self.tree.delete(*self.tree.get_children())
        for b in books:
            self.tree.insert(
                "", "end",
                values=(
                    b.get("bookID"),
                    b.get("title"),
                    b.get("authors"),
                    b.get("isbn"),
                    b.get("Status"),
                    b.get("Checkouts"),
                )
            )

    def filter_books(self, *_):
        q = self.search_var.get().lower()
        filtered = [
            b for b in self.all_books
            if q in b.get("title", "").lower()
            or q in b.get("isbn", "").lower()
        ]
        self.refresh(filtered)

    # -------------------------------------------------
    def add_book(self):
        dlg = ctk.CTkToplevel(self)
        dlg.title("Add Book")
        dlg.geometry("400x450")
        dlg.configure(fg_color=BG_DARK)
        dlg.grab_set()

        entries = {}
        for f in ["Title", "Authors", "ISBN", "Publisher", "Pages", "Year"]:
            ctk.CTkLabel(dlg, text=f).pack(pady=(10, 0))
            e = ctk.CTkEntry(
                dlg,
                width=ENTRY_WIDTH,
                font=FONT_INPUT
                )
            e.pack(pady=6)
            entries[f] = e

        def save():
            max_id = max(
                [int(b["bookID"]) for b in self.all_books if b["bookID"].isdigit()],
                default=0
            )
            new_book = {
                "bookID": str(max_id + 1),
                "title": entries["Title"].get(),
                "authors": entries["Authors"].get(),
                "isbn": entries["ISBN"].get(),
                "publisher": entries["Publisher"].get(),
                "num_pages": entries["Pages"].get(),
                "publication_date": entries["Year"].get(),
                "Status": "Available",
                "Checkouts": "0",
                "average_rating": "0",
                "isbn13": "",
                "language_code": "eng",
                "ratings_count": "0",
                "text_reviews_count": "0",
            }

            if not new_book["title"]:
                messagebox.showerror("Error", "Title required")
                return

            self.all_books.append(new_book)

            DataHandler.write_csv(
                BOOKS_PATH,
                self.all_books,
                [
                    "bookID","title","authors","average_rating","isbn",
                    "isbn13","language_code","num_pages","ratings_count",
                    "text_reviews_count","publication_date","publisher",
                    "Status","Checkouts"
                ]
            )

            dlg.destroy()
            self.refresh(self.all_books)

        ctk.CTkButton(dlg, text="Save Book", command=save).pack(pady=20)

    # -------------------------------------------------
    def remove_book(self):
        sel = self.tree.selection()
        if not sel:
            return

        if not messagebox.askyesno("Confirm", "Remove selected book?"):
            return

        book_id = str(self.tree.item(sel[0])["values"][0])
        self.all_books = [
            b for b in self.all_books if str(b["bookID"]) != book_id
        ]

        DataHandler.write_csv(
            BOOKS_PATH,
            self.all_books,
            [
                "bookID","title","authors","average_rating","isbn",
                "isbn13","language_code","num_pages","ratings_count",
                "text_reviews_count","publication_date","publisher",
                "Status","Checkouts"
            ]
        )

        self.refresh(self.all_books)

    # -------------------------------------------------
    def edit_status(self):
        sel = self.tree.selection()
        if not sel:
            return

        dlg = ctk.CTkToplevel(self)
        dlg.title("Edit Status")
        dlg.geometry("300x200")
        dlg.configure(fg_color=BG_DARK)
        dlg.grab_set()

        status = tk.StringVar(value="Available")
        ctk.CTkOptionMenu(
            dlg, variable=status,
            values=["Available", "Checked Out", "Reserved", "Lost"]
        ).pack(pady=40)

        def update():
            book_id = str(self.tree.item(sel[0])["values"][0])
            for b in self.all_books:
                if str(b["bookID"]) == book_id:
                    b["Status"] = status.get()

            DataHandler.write_csv(
                BOOKS_PATH,
                self.all_books,
                [
                    "bookID","title","authors","average_rating","isbn",
                    "isbn13","language_code","num_pages","ratings_count",
                    "text_reviews_count","publication_date","publisher",
                    "Status","Checkouts"
                ]
            )

            dlg.destroy()
            self.refresh(self.all_books)

        ctk.CTkButton(dlg, text="Update Status", command=update).pack(pady=20)
# =====================================================
# PATRONS MANAGEMENT
# =====================================================
class PatronsManagement(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller

        tk.Label(
            self, text="Patrons & Circulation",
            font=("Segoe UI", 18, "bold"),
            bg=BG_DARK, fg=FG_TEXT
        ).pack(anchor="w", pady=10)

        controls = tk.Frame(self, bg=BG_DARK)
        controls.pack(fill="x", pady=5)

        ctk.CTkButton(
            controls, text="+ Add Patron",
            command=self.add_patron
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            controls, text="Remove Patron",
            fg_color="#a83232",
            command=self.remove_patron
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            controls, text="Edit Patron Info",
            fg_color="#c47a2c",
            command=self.edit_patron
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            controls, text="Lend Book",
            command=self.lend_book
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            controls, text="Receive Book",
            fg_color="#6a3fc4",
            command=self.receive_book
            ).pack(side="left", padx=5)


        # ---------------- TABLE ----------------
        table_frame = tk.Frame(self, bg=BG_TABLE)
        table_frame.pack(fill="both", expand=True, pady=10)

        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview",
            background=BG_TABLE,
            foreground=FG_TEXT,
            fieldbackground=BG_TABLE,
            font=TABLE_FONT,
            rowheight=34
        )

        style.configure(
            "Treeview.Heading",
            font=TABLE_HEADER_FONT
        )

        style.map(
            "Treeview",
            background=[("selected", ACCENT)]
        )

        style.map("Treeview", background=[("selected", ACCENT)])

        cols = ("Name", "Library #", "Age", "Type", "Fines", "Borrowed")
        self.tree = ttk.Treeview(
            table_frame, columns=cols,
            show="headings", height=20
        )

        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="w")

        self.tree.pack(fill="both", expand=True)

        self.all_patrons = DataHandler.read_csv(PATRONS_PATH)
        self.refresh()

    # -------------------------------------------------
    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for p in self.all_patrons:
            borrowed = 0
            try:
                borrowed = len(json.loads(p.get("borrowed_books", "{}")))
            except:
                pass

            ptype = p.get("object", "").split("(")[0]

            self.tree.insert(
                "", "end",
                values=(
                    p.get("name"),
                    p.get("library_number"),
                    p.get("age"),
                    ptype,
                    f"${float(p.get('fines', 0)):.2f}",
                    borrowed
                )
            )

    # -------------------------------------------------
    def add_patron(self):
        dlg = ctk.CTkToplevel(self)
        dlg.title("Add Patron")
        dlg.geometry("350x450")
        dlg.configure(fg_color=BG_DARK)
        dlg.grab_set()

        ctk.CTkLabel(dlg, text="Name").pack(pady=(10, 0))
        e = ctk.CTkEntry(
            dlg,
            width=ENTRY_WIDTH,
            font=FONT_INPUT
        )
        e.pack(pady=6)

        ctk.CTkLabel(dlg, text="Age").pack(pady=(10, 0))
        e = ctk.CTkEntry(
            dlg,
            width=ENTRY_WIDTH,
            font=FONT_INPUT
        )
        e.pack(pady=6)

        ctk.CTkLabel(dlg, text="Type").pack(pady=(10, 0))
        ptype = tk.StringVar(value="Student")
        ctk.CTkOptionMenu(
            dlg, variable=ptype,
            values=["Student", "Faculty", "Community", "Child"]
        ).pack(pady=5)

        def save():
            try:
                age = int(e_age.get())
                if age < 0:
                    raise ValueError
            except:
                messagebox.showerror("Error", "Invalid age")
                return

            if ptype.get() == "Child" and age > 12:
                messagebox.showerror("Error", "Child must be 12 or younger")
                return

            limits = {
                "Student": (5, 30),
                "Faculty": (10, 60),
                "Community": (3, 20),
                "Child": (2, 15)
            }

            max_b, max_d = limits[ptype.get()]

            new_patron = {
                "name": e_name.get(),
                "age": age,
                "library_number": DataHandler.generate_id(),
                "fines": "0",
                "days_overdue": "0",
                "max_books_allowed": max_b,
                "max_days_allowed": max_d,
                "contact_number": "",
                "book_preferences": "",
                "borrowed_books": "{}",
                "object": f"{ptype.get()}({e_name.get()})"
            }

            self.all_patrons.append(new_patron)

            DataHandler.write_csv(
                PATRONS_PATH,
                self.all_patrons,
                [
                    "name","age","library_number","fines","days_overdue",
                    "max_books_allowed","max_days_allowed","contact_number",
                    "book_preferences","borrowed_books","object"
                ]
            )

            dlg.destroy()
            self.refresh()

        ctk.CTkButton(dlg, text="Save Patron", command=save).pack(pady=20)

    # -------------------------------------------------
    def remove_patron(self):
        sel = self.tree.selection()
        if not sel:
            return

        if not messagebox.askyesno("Confirm", "Remove selected patron?"):
            return

        lib_num = str(self.tree.item(sel[0])["values"][1])
        self.all_patrons = [
            p for p in self.all_patrons
            if str(p["library_number"]) != lib_num
        ]

        DataHandler.write_csv(
            PATRONS_PATH,
            self.all_patrons,
            [
                "name","age","library_number","fines","days_overdue",
                "max_books_allowed","max_days_allowed","contact_number",
                "book_preferences","borrowed_books","object"
            ]
        )

        self.refresh()

    # -------------------------------------------------
    def edit_patron(self):
        sel = self.tree.selection()
        if not sel:
            def big_popup(title, message):
                dlg = ctk.CTkToplevel()
                dlg.title(title)
                dlg.geometry("420x200")
                dlg.grab_set()

                ctk.CTkLabel(
                    dlg,
                    text=message,
                    font=("Segoe UI", 15),
                    wraplength=360,
                    justify="center"
                ).pack(expand=True, pady=30)

                ctk.CTkButton(
                    dlg,
                    text="OK",
                    width=120,
                    command=dlg.destroy
                ).pack(pady=10)

            return

        lib_num = str(self.tree.item(sel[0])["values"][1])
        patron = next(
            (p for p in self.all_patrons if str(p["library_number"]) == lib_num),
            None
        )

        if not patron:
            return

        dlg = ctk.CTkToplevel(self)
        dlg.title("Edit Patron")
        dlg.geometry("350x450")
        dlg.configure(fg_color=BG_DARK)
        dlg.grab_set()

        fields = [
            "name","age","contact_number",
            "book_preferences","max_books_allowed","max_days_allowed"
        ]
        entries = {}

        for f in fields:
            ctk.CTkLabel(dlg, text=f.replace("_", " ").title()).pack(pady=(10, 0))
            e = ctk.CTkEntry(dlg)
            e.insert(0, str(patron.get(f, "")))
            e.pack(fill="x", padx=30)
            entries[f] = e

        def save():
            try:
                int(entries["age"].get())
                int(entries["max_books_allowed"].get())
                int(entries["max_days_allowed"].get())
            except:
                messagebox.showerror("Error", "Invalid numeric values")
                return

            for f in fields:
                patron[f] = entries[f].get()

            DataHandler.write_csv(
                PATRONS_PATH,
                self.all_patrons,
                [
                    "name","age","library_number","fines","days_overdue",
                    "max_books_allowed","max_days_allowed","contact_number",
                    "book_preferences","borrowed_books","object"
                ]
            )

            dlg.destroy()
            self.refresh()

        ctk.CTkButton(dlg, text="Update Patron", command=save).pack(pady=20)

# =====================================================
# LENDING & RETURNING
# =====================================================
    def lend_book(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a patron first")
            return

        lib_num = str(self.tree.item(sel[0])["values"][1])
        patron = next(
            (p for p in self.all_patrons if str(p["library_number"]) == lib_num),
            None
        )
        if not patron:
            return

        borrowed = json.loads(patron.get("borrowed_books", "{}"))
        if len(borrowed) >= int(patron["max_books_allowed"]):
            messagebox.showerror(
                "Limit Reached",
                f"Patron can only borrow {patron['max_books_allowed']} books"
            )
            return

        book_id = simpledialog.askstring("Lend Book", "Enter Book ID:")
        if not book_id:
            return

        books = DataHandler.read_csv(BOOKS_PATH)
        book = next((b for b in books if str(b["bookID"]) == book_id), None)

        if not book:
            messagebox.showerror("Error", "Book not found")
            return

        if book["Status"] == "Checked Out":
            messagebox.showerror("Unavailable", "Book already checked out")
            return

        today = datetime.date.today()
        due = today + datetime.timedelta(days=int(patron["max_days_allowed"]))

        borrowed[book["isbn"]] = {
            "bookID": book_id,
            "title": book["title"],
            "checkout_date": str(today),
            "due_date": str(due),
            "isbn": book["isbn"]
        }

        patron["borrowed_books"] = json.dumps(borrowed)

        book["Status"] = "Checked Out"
        book["Checkouts"] = str(int(book.get("Checkouts", 0)) + 1)

        DataHandler.write_csv(
            PATRONS_PATH,
            self.all_patrons,
            [
                "name","age","library_number","fines","days_overdue",
                "max_books_allowed","max_days_allowed","contact_number",
                "book_preferences","borrowed_books","object"
            ]
        )

        DataHandler.write_csv(
            BOOKS_PATH,
            books,
            [
                "bookID","title","authors","average_rating","isbn",
                "isbn13","language_code","num_pages","ratings_count",
                "text_reviews_count","publication_date","publisher",
                "Status","Checkouts"
            ]
        )

        DataHandler.log_transaction(
            "lend",
            self.controller.current_user["username"],
            lib_num,
            book_id,
            0,
            f"Lent {book['title']}"
        )

        def big_popup(title, message):
            dlg = ctk.CTkToplevel()
            dlg.title(title)
            dlg.geometry("420x200")
            dlg.grab_set()

            ctk.CTkLabel(
                dlg,
                text=message,
                font=("Segoe UI", 15),
                wraplength=360,
                justify="center"
            ).pack(expand=True, pady=30)

            ctk.CTkButton(
                dlg,
                text="OK",
                width=120,
                command=dlg.destroy
            ).pack(pady=10)

        self.refresh()

    # -------------------------------------------------
    def receive_book(self):
        book_id = simpledialog.askstring("Return Book", "Enter Book ID:")
        if not book_id:
            return

        target_patron = None
        target_isbn = None

        for p in self.all_patrons:
            borrowed = json.loads(p.get("borrowed_books", "{}"))
            for isbn, info in borrowed.items():
                if str(info.get("bookID")) == book_id:
                    target_patron = p
                    target_isbn = isbn
                    break
            if target_patron:
                break

        if not target_patron:
            messagebox.showerror("Error", "Book not found in loans")
            return

        borrowed = json.loads(target_patron["borrowed_books"])
        del borrowed[target_isbn]
        target_patron["borrowed_books"] = json.dumps(borrowed)

        DataHandler.write_csv(
            PATRONS_PATH,
            self.all_patrons,
            [
                "name","age","library_number","fines","days_overdue",
                "max_books_allowed","max_days_allowed","contact_number",
                "book_preferences","borrowed_books","object"
            ]
        )

        books = DataHandler.read_csv(BOOKS_PATH)
        for b in books:
            if str(b["bookID"]) == book_id:
                b["Status"] = "Available"

        DataHandler.write_csv(
            BOOKS_PATH,
            books,
            [
                "bookID","title","authors","average_rating","isbn",
                "isbn13","language_code","num_pages","ratings_count",
                "text_reviews_count","publication_date","publisher",
                "Status","Checkouts"
            ]
        )

        DataHandler.log_transaction(
            "receive",
            self.controller.current_user["username"],
            target_patron["library_number"],
            book_id,
            0,
            "Returned"
        )

        def big_popup(title, message):
            dlg = ctk.CTkToplevel()
            dlg.title(title)
            dlg.geometry("420x200")
            dlg.grab_set()

            ctk.CTkLabel(
                dlg,
                text=message,
                font=("Segoe UI", 15),
                wraplength=360,
                justify="center"
            ).pack(expand=True, pady=30)

            ctk.CTkButton(
                dlg,
                text="OK",
                width=120,
                command=dlg.destroy
            ).pack(pady=10)

        self.refresh()

# =====================================================
# REPORTS & FINES
# =====================================================
class ReportsManagement(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller

        tk.Label(
            self, text="Reports & Fines",
            font=("Segoe UI", 18, "bold"),
            bg=BG_DARK, fg=FG_TEXT
        ).pack(anchor="w", pady=10)

        controls = tk.Frame(self, bg=BG_DARK)
        controls.pack(fill="x", pady=5)

        ctk.CTkButton(
            controls, text="Calculate Overdue Fines",
            command=self.calculate_overdue
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            controls, text="Receive Fine Payment",
            fg_color="#2d8a44",
            command=self.receive_fine
        ).pack(side="left", padx=5)

        # ---------------- TABLE ----------------
        table_frame = tk.Frame(self, bg=BG_TABLE)
        table_frame.pack(fill="both", expand=True, pady=10)

        style = ttk.Style()
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview",
            background=BG_TABLE,
            foreground=FG_TEXT,
            fieldbackground=BG_TABLE,
            font=TABLE_FONT,
            rowheight=34
        )

        style.configure(
            "Treeview.Heading",
            font=TABLE_HEADER_FONT
        )

        style.map(
            "Treeview",
            background=[("selected", ACCENT)]
        )

        style.map("Treeview", background=[("selected", ACCENT)])

        cols = ("Time", "Type", "Actor", "Patron", "Book", "Amount", "Note")
        self.tree = ttk.Treeview(
            table_frame, columns=cols, show="headings"
        )

        for c in cols:
            self.tree.heading(c, text=c)

        self.tree.column("Note", width=280)
        self.tree.pack(fill="both", expand=True)

        self.load_transactions()

    def load_transactions(self):
        self.tree.delete(*self.tree.get_children())
        if not os.path.exists(TRANSACTIONS_PATH):
            return
        with open(TRANSACTIONS_PATH, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reversed(list(reader)[-100:]):
                self.tree.insert("", "end", values=row)

    def calculate_overdue(self):
        def big_popup(title, message):
            dlg = ctk.CTkToplevel()
            dlg.title(title)
            dlg.geometry("420x200")
            dlg.grab_set()

            ctk.CTkLabel(
                dlg,
                text=message,
                font=("Segoe UI", 15),
                wraplength=360,
                justify="center"
            ).pack(expand=True, pady=30)

            ctk.CTkButton(
                dlg,
                text="OK",
                width=120,
                command=dlg.destroy
            ).pack(pady=10)


    def receive_fine(self):
        lib = simpledialog.askstring("Fine Payment", "Enter Patron Library Number:")
        if not lib:
            return

        patrons = DataHandler.read_csv(PATRONS_PATH)
        patron = next((p for p in patrons if str(p["library_number"]) == lib), None)

        if not patron:
            messagebox.showerror("Error", "Patron not found")
            return

        owed = float(patron.get("fines", 0))
        if owed <= 0:
            def big_popup(title, message):
                dlg = ctk.CTkToplevel()
                dlg.title(title)
                dlg.geometry("420x200")
                dlg.grab_set()

                ctk.CTkLabel(
                    dlg,
                    text=message,
                    font=("Segoe UI", 15),
                    wraplength=360,
                    justify="center"
                ).pack(expand=True, pady=30)

                ctk.CTkButton(
                    dlg,
                    text="OK",
                    width=120,
                    command=dlg.destroy
                ).pack(pady=10)

            return

        amt = simpledialog.askstring("Payment", f"Owed ${owed:.2f}\nEnter amount:")
        try:
            amt = float(amt)
        except:
            return

        if amt > owed:
            messagebox.showerror("Error", "Cannot overpay")
            return

        patron["fines"] = str(owed - amt)

        DataHandler.write_csv(
            PATRONS_PATH,
            patrons,
            [
                "name","age","library_number","fines","days_overdue",
                "max_books_allowed","max_days_allowed","contact_number",
                "book_preferences","borrowed_books","object"
            ]
        )

        DataHandler.log_transaction(
            "fine_payment",
            self.controller.current_user["username"],
            lib,
            "",
            amt,
            "Fine Paid"
        )

        self.load_transactions()
        def big_popup(title, message):
            dlg = ctk.CTkToplevel()
            dlg.title(title)
            dlg.geometry("420x200")
            dlg.grab_set()

            ctk.CTkLabel(
                dlg,
                text=message,
                font=("Segoe UI", 15),
                wraplength=360,
                justify="center"
            ).pack(expand=True, pady=30)

            ctk.CTkButton(
                dlg,
                text="OK",
                width=120,
                command=dlg.destroy
            ).pack(pady=10)


# =====================================================
# STAFF MANAGEMENT
# =====================================================
class StaffManagement(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_DARK)
        self.controller = controller

        tk.Label(
            self, text="Staff Management",
            font=("Segoe UI", 18, "bold"),
            bg=BG_DARK, fg=FG_TEXT
        ).pack(anchor="w", pady=10)

        controls = tk.Frame(self, bg=BG_DARK)
        controls.pack(fill="x", pady=5)

        ctk.CTkButton(
            controls, text="+ Add Assistant",
            command=self.add_assistant
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            controls, text="Remove Assistant",
            fg_color="#a83232",
            command=self.remove_assistant
        ).pack(side="left", padx=5)

        # ---------------- TABLE ----------------
        table_frame = tk.Frame(self, bg=BG_TABLE)
        table_frame.pack(fill="both", expand=True, pady=10)

        style = ttk.Style()
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview",
            background=BG_TABLE,
            foreground=FG_TEXT,
            fieldbackground=BG_TABLE,
            font=TABLE_FONT,
            rowheight=34
        )

        style.configure(
            "Treeview.Heading",
            font=TABLE_HEADER_FONT
        )

        style.map(
            "Treeview",
            background=[("selected", ACCENT)]
        )

        style.map("Treeview", background=[("selected", ACCENT)])

        cols = ("Name", "Age", "Username")
        self.tree = ttk.Treeview(
            table_frame, columns=cols, show="headings"
        )

        for c in cols:
            self.tree.heading(c, text=c)

        self.tree.pack(fill="both", expand=True)

        self.load_staff()

    def load_staff(self):
        self.tree.delete(*self.tree.get_children())
        self.staff = DataHandler.read_csv(ASSISTANTS_PATH)
        for a in self.staff:
            self.tree.insert(
                "", "end",
                values=(a["name"], a["age"], a["username"])
            )

    def add_assistant(self):
        username = simpledialog.askstring("Add Assistant", "Username:")
        if not username:
            return

        if any(a["username"] == username for a in self.staff):
            messagebox.showerror("Error", "Username already exists")
            return

        name = simpledialog.askstring("Add Assistant", "Name:")
        age = simpledialog.askstring("Add Assistant", "Age:")
        password = simpledialog.askstring("Add Assistant", "Password:")

        with open(ASSISTANTS_PATH, "a", newline="") as f:
            csv.writer(f).writerow([
                name, age, username, password,
                DataHandler.generate_id(), "Assistant"
            ])

        self.load_staff()

    def remove_assistant(self):
        sel = self.tree.selection()
        if not sel:
            return

        username = self.tree.item(sel[0])["values"][2]
        self.staff = [
            a for a in self.staff if a["username"] != username
        ]

        DataHandler.write_csv(
            ASSISTANTS_PATH,
            self.staff,
            ["name","age","username","password","library_number","object"]
        )

        self.load_staff()

# =====================================================
# MAIN APPLICATION
# =====================================================
class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("1200x700")
        self.configure(fg_color=BG_DARK)

        self.current_user = None
        self.user_role = None

        container = tk.Frame(self, bg=BG_DARK)
        container.pack(fill="both", expand=True)
        self.container = container

        self.show_startup()

    def clear(self):
        for w in self.container.winfo_children():
            w.destroy()

    def show_startup(self):
        self.clear()
        if not DataHandler.read_csv(LIBRARIANS_PATH):
            RegisterLibrarianFrame(self.container, self).pack(fill="both", expand=True)
        else:
            LoginFrame(self.container, self).pack(fill="both", expand=True)

    def login_success(self, user, role):
        self.current_user = user
        self.user_role = role
        self.clear()
        DashboardFrame(self.container, self).pack(fill="both", expand=True)

    def logout(self):
        self.current_user = None
        self.user_role = None
        self.show_startup()
# =====================================================
# ENTRY POINT
# =====================================================
if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()