# 📚 Library Management System

Welcome to the **Library Management System** - a powerful and user-friendly tool designed to help you manage your library efficiently. Whether you're running a school library, community library, or any book lending service, this system has everything you need!

## 🌟 What is This?

The Library Management System is a complete solution for managing books, patrons (library members), staff, and all library operations. It comes in **two versions**:

1. **Command-Line Interface (CLI)** - A text-based interface perfect for quick operations
2. **Graphical User Interface (GUI)** - A modern, visual interface with a beautiful dark theme

Both versions offer the same powerful features, so choose the one that suits your preference!

---

## 🚀 Getting Started

### What You Need

Before you begin, make sure you have:
- **Python 3.7 or newer** installed on your computer
- The `books123.updated.csv` file (your book database)

### Installation Steps

1. **Download the System**
   - Download all files from this repository to a folder on your computer

2. **Install Required Components**
   - Open your terminal or command prompt
   - Navigate to the folder where you downloaded the files
   - The system will automatically install any missing components when you first run it!

3. **Prepare Your Book Database**
   - Make sure `books123.updated.csv` is in the same folder as the program files
   - This file contains all your library's books

---

## 💻 How to Run the System

### Running the Command-Line Version

1. Open your terminal or command prompt
2. Navigate to the folder containing the system files
3. Type: `python "project librarian.py"`
4. Press Enter and follow the on-screen instructions!

### Running the Graphical Version

1. Open your terminal or command prompt
2. Navigate to the folder containing the system files
3. Type: `python "library gui version.py"`
4. Press Enter and enjoy the beautiful interface!

---

## 👥 User Types

The system supports three types of users, each with different access levels:

### 1. **Librarian** (Full Access)
- Complete control over the entire system
- Can manage books, patrons, assistants, and generate reports
- **First Time Setup**: If no librarian account exists, you'll be guided to create one

### 2. **Assistant** (Limited Access)
- Can handle day-to-day library operations
- Manages book lending, returns, and patron information
- Cannot add/remove other staff members
- **Note**: Only librarians can create assistant accounts

### 3. **Patron** (Library Members)
- Four types of patrons with different borrowing limits:
  - **Student**: Borrow up to 5 books for 30 days
  - **Faculty**: Borrow up to 10 books for 60 days
  - **Community Member**: Borrow up to 3 books for 20 days
  - **Child** (12 years or younger): Borrow up to 2 books for 15 days

---

## 📖 Main Features

### 📚 Book Management

**What You Can Do:**
- **Add New Books**: Register new books in your library collection
  - Enter book details: title, author, ISBN, publisher, publication year, and pages
  - Each book gets a unique ID automatically
  
- **Search Books**: Find books quickly by:
  - Book ID number
  - Title (partial matches work!)
  - ISBN number
  
- **Edit Book Status**: Change book status to:
  - Available (ready to lend)
  - Checked Out (currently borrowed)
  - Reserved (held for someone)
  - Lost (missing from collection)
  
- **Remove Books**: Remove books from your collection when needed

### 👤 Patron (Member) Management

**What You Can Do:**
- **Register New Patrons**: Add new library members
  - Choose patron type (Student, Faculty, Community, or Child)
  - Enter name, age, and contact information
  - System automatically assigns borrowing limits based on type
  
- **View Patron Information**: See all details about library members:
  - Personal information
  - Currently borrowed books
  - Outstanding fines
  - Days overdue
  
- **Edit Patron Details**: Update member information as needed
  - Change contact information
  - Update book preferences
  - Adjust borrowing limits
  
- **Remove Patrons**: Remove members from the system when needed

### 📖 Lending & Returns

**How It Works:**

**Lending a Book:**
1. Enter the patron's library number
2. Enter the book ID you want to lend
3. System automatically:
   - Checks if patron has reached their borrowing limit
   - Verifies book is available
   - Sets the due date based on patron type
   - Updates book status to "Checked Out"
   - Records the transaction

**Returning a Book:**
1. Enter the book ID being returned
2. System automatically:
   - Marks book as "Available"
   - Removes it from patron's borrowed books
   - Records the transaction
   - Calculates any overdue fines

### 💰 Fine Management

**Understanding Fines:**
- **Fine Rate**: ₱5 per day for overdue books
- Fines are calculated automatically when books are late

**What You Can Do:**
- **Calculate Overdue Fines**: Run a calculation to update all fines
  - System checks all borrowed books
  - Calculates days overdue
  - Updates fine amounts for each patron
  
- **Receive Fine Payments**: Process payments from patrons
  - Enter patron's library number
  - See their current fine amount
  - Enter payment amount
  - System updates their balance

### 👔 Staff Management (Librarians Only)

**What Librarians Can Do:**
- **Add Assistants**: Create new assistant accounts
  - Set username and password
  - Assistants can help with daily operations
  
- **View All Assistants**: See list of all assistant staff
  
- **Remove Assistants**: Remove assistant accounts when needed

### 📊 Reports & Analytics

**Available Reports:**

1. **Transaction History**
   - View recent library activities
   - See who borrowed or returned books
   - Track fine payments
   - Monitor staff actions

2. **Full Library Report** (includes):
   - **Inventory Summary**:
     - Total number of books
     - Books currently checked out
     - Books available
     - Circulation rate (how often books are borrowed)
     - Average book age
     - Books eligible for removal (over 10 years old)
   
   - **Circulation Activity**:
     - Total checkouts across all books
     - Most popular books
   
   - **Patron Statistics**:
     - Number of active patrons (those with borrowed books)
     - Average books borrowed per patron
   
   - **Financial Report**:
     - Total outstanding fines
     - Total fines collected

### 🔒 Account Security

**Password Management:**
- **Change Password**: Update your password anytime
  - Enter current password to confirm
  - Set new password
  
- **Forgot Password** (Librarians Only):
  - Use the secret password from the video demo
  - Retrieve your login credentials

**Account Deletion:**
- Delete your own account when needed
- **Warning**: This cannot be undone!

---

## 🎯 Common Tasks & How to Do Them

### First Time Setup

**For Your Very First Use:**
1. Run the program
2. Since no accounts exist, you'll see: "Welcome to the Library Management System - Since there is no accounts yet..."
3. Create your librarian account:
   - Enter your name
   - Enter your age
   - Choose a username
   - Create a password
4. You're ready to start managing your library!

### Daily Operations

**Morning Routine:**
1. Log in to the system
2. Run "Calculate Overall Fines" to update all overdue fines
3. Check "Transaction History" to see what happened yesterday

**When a Patron Wants to Borrow a Book:**
1. Search for the book to verify it's available
2. Select "Lend Book"
3. Enter patron's library number
4. Enter the book ID
5. Done! The system handles everything else

**When a Patron Returns a Book:**
1. Select "Receive Book" or "Return Book"
2. Enter the book ID
3. System updates everything automatically
4. If there are fines, process payment using "Receive Fines"

### Weekly Tasks

**End of Week Review:**
1. Generate a "Full Library Report"
2. Review outstanding fines
3. Check most borrowed books
4. Review circulation statistics

---

## 💡 Tips & Best Practices

### For Librarians

✅ **Do's:**
- Create assistant accounts for staff to share the workload
- Run fine calculations daily to keep records current
- Generate reports weekly to track library performance
- Back up your CSV files regularly (they contain all your data)
- Keep the books database file in the same folder as the program

❌ **Don'ts:**
- Don't delete CSV files while the program is running
- Don't share your librarian password
- Don't manually edit CSV files (use the program instead)
- Don't forget to log out when finished

### For Assistants

✅ **Do's:**
- Always verify book IDs before lending
- Check patron borrowing limits before lending books
- Process fine payments accurately
- Record all transactions properly

❌ **Don'ts:**
- Don't forget to mark books as returned
- Don't manually change book statuses without checking with a librarian

### Search Tips

**Finding Books Faster:**
- Use partial titles: searching for "harry" will find "Harry Potter"
- Book ID search is fastest - use it when you know the number
- ISBN search is most accurate for exact matches

---

## 🆘 Troubleshooting

### Common Issues & Solutions

**Problem**: "INSTALL books123.updated.csv FIRST"
- **Solution**: The books database file is missing. Download `books123.updated.csv` and place it in the same folder as the program.

**Problem**: Program won't start or shows errors about missing modules
- **Solution**: 
  - For GUI version: The program will automatically install `customtkinter`
  - For CLI version: All required modules come with Python

**Problem**: "Invalid username or password"
- **Solution**: 
  - Check for typos (username and password are case-sensitive)
  - Librarians can use the "Forgot Password" option with the secret code from the video
  - Assistants must contact a librarian for password help

**Problem**: Can't lend a book to a patron
- **Possible Reasons**:
  - Patron reached their borrowing limit (check patron info)
  - Book is not available (check book status)
  - Book ID is incorrect (verify the book ID)

**Problem**: Fines not calculating correctly
- **Solution**: Run "Calculate Overall Fines" to update all fine amounts

**Problem**: GUI window is too small or elements overlap
- **Solution**: Resize the window - the GUI adapts to different sizes

---

## 📁 Data Files Explained

The system uses CSV files to store data. Here's what each file contains:

- **books123.updated.csv**: All books in your library
- **patron1.csv**: All library members and their information
- **librarian1.csv**: Librarian accounts
- **assistant1.csv**: Assistant accounts
- **transactions.csv**: Record of all library activities

**Important**: These files are created automatically. Don't delete them unless you want to reset the system!

---

## 🎨 GUI Features (Graphical Version Only)

### Beautiful Dark Theme Interface
- Modern, easy-on-the-eyes design
- Large, readable text
- Color-coded actions (blue for normal, red for delete, green for positive actions)

### Organized Tabs
- **Books Tab**: Manage your book collection
- **Patrons Tab**: Handle member operations and lending/returns
- **Reports & Fines Tab**: View financial data and generate reports
- **Staff Tab**: Manage assistants (librarians only)

### Quick Actions
- Buttons for all common tasks
- Search functionality in Books tab
- Select and click to perform actions
- Visual feedback for all operations

---

## 🔐 Security Features

- **Secure Login System**: Separate accounts for librarians and assistants
- **Password Protection**: All accounts are password-protected
- **Role-Based Access**: Different users can only access features they need
- **Transaction Logging**: Every action is recorded with timestamp and user info
- **Account Deletion Safety**: Requires confirmation to prevent accidents

---

## 📞 Need Help?

### During Setup
- Make sure Python 3.7+ is installed
- Verify `books123.updated.csv` is in the correct folder
- Run the program and follow the first-time setup wizard

### During Use
- Read the on-screen instructions carefully
- Press 'B' or 'Cancel' to go back in most menus
- Check the transaction history if you're unsure about recent actions
- Generate a report to see overall system status

### For Librarians
- Watch the video demo for the secret password feature
- Back up your CSV files regularly
- Keep track of all assistant accounts you create

---

## 🎓 Quick Reference

### Keyboard Shortcuts (CLI Version)
- **B**: Go back to previous menu
- **Enter**: Confirm action or continue

### Status Values for Books
- **Available**: Book can be borrowed
- **Checked Out**: Book is currently borrowed
- **Reserved**: Book is reserved for a patron
- **Lost**: Book is missing from collection

### Fine Calculation
- **Rate**: ₱5 per day
- **When Charged**: Automatically calculated when book is overdue
- **Payment**: Can be partial or full amount

---

## ✨ Congratulations!

You now know everything you need to efficiently manage your library using this system. Whether you prefer the quick CLI version or the beautiful GUI version, you have all the tools to:

- Organize your book collection
- Manage library members
- Handle lending and returns
- Track fines and payments
- Generate helpful reports
- Manage your staff

**Happy Librar-ing! 📚✨**

---

## 📄 Version Information

- **Current Version**: 3.0
- **GUI Framework**: CustomTkinter (automatically installed)
- **Python Compatibility**: Python 3.7+
- **Platforms**: Windows, macOS, Linux

---

*For developers or those interested in modifying the system, please refer to the source code files: `project librarian.py` (CLI version) and `library gui version.py` (GUI version).*
