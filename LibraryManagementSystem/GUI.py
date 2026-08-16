import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox


# ================= DATABASE SETUP =================

def create_database():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            author TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ================= CLEAR FIELDS =================

def clear_fields():
    book_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)


# ================= ADD BOOK =================

def add_book():

    name = book_entry.get()
    author = author_entry.get()
    quantity = quantity_entry.get()

    if name == "" or author == "" or quantity == "":
        messagebox.showwarning(
            "Warning",
            "Please fill all fields."
        )
        return

    try:
        quantity = int(quantity)

        if quantity < 0:
            messagebox.showerror(
                "Error",
                "Quantity cannot be negative."
            )
            return

    except ValueError:
        messagebox.showerror(
            "Error",
            "Quantity must be a number."
        )
        return

    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO books (name, author, quantity)
        VALUES (?, ?, ?)
        """,
        (name, author, quantity)
    )

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        "Book added successfully!"
    )

    clear_fields()
    view_books()


# ================= VIEW BOOKS =================

def view_books():

    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    conn.close()

    # Clear old table data
    for row in table.get_children():
        table.delete(row)

    # Add database data to table
    for book in books:
        table.insert(
            "",
            tk.END,
            values=book
        )


# ================= SEARCH BOOK =================

def search_book():

    name = book_entry.get()

    if name == "":
        messagebox.showwarning(
            "Warning",
            "Enter a book name to search."
        )
        return

    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM books
        WHERE name LIKE ?
        """,
        ("%" + name + "%",)
    )

    books = cursor.fetchall()

    conn.close()

    # Clear table
    for row in table.get_children():
        table.delete(row)

    # Display search results
    for book in books:
        table.insert(
            "",
            tk.END,
            values=book
        )

    if len(books) == 0:
        messagebox.showinfo(
            "Result",
            "No book found."
        )


# ================= SELECT BOOK =================

def select_book(event):

    selected = table.selection()

    if not selected:
        return

    book = table.item(
        selected[0],
        "values"
    )

    clear_fields()

    book_entry.insert(
        0,
        book[1]
    )

    author_entry.insert(
        0,
        book[2]
    )

    quantity_entry.insert(
        0,
        book[3]
    )


# ================= UPDATE BOOK =================

def update_book():

    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Select a book to update."
        )
        return

    book = table.item(
        selected[0],
        "values"
    )

    book_id = book[0]

    name = book_entry.get()
    author = author_entry.get()
    quantity = quantity_entry.get()

    if name == "" or author == "" or quantity == "":
        messagebox.showwarning(
            "Warning",
            "Please fill all fields."
        )
        return

    try:
        quantity = int(quantity)

        if quantity < 0:
            messagebox.showerror(
                "Error",
                "Quantity cannot be negative."
            )
            return

    except ValueError:
        messagebox.showerror(
            "Error",
            "Quantity must be a number."
        )
        return

    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE books
        SET name = ?, author = ?, quantity = ?
        WHERE id = ?
        """,
        (name, author, quantity, book_id)
    )

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        "Book updated successfully!"
    )

    clear_fields()
    view_books()


# ================= DELETE BOOK =================

def delete_book():

    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Select a book to delete."
        )
        return

    book = table.item(
        selected[0],
        "values"
    )

    book_id = book[0]

    answer = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this book?"
    )

    if not answer:
        return

    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM books WHERE id = ?",
        (book_id,)
    )

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        "Book deleted successfully!"
    )

    clear_fields()
    view_books()


# ================= CREATE DATABASE =================

create_database()


# ================= MAIN WINDOW =================

window = tk.Tk()

window.title("Library Manager")
window.geometry("650x600")


# ================= BOOK NAME =================

book_label = tk.Label(
    window,
    text="Book Name:"
)

book_label.grid(
    row=0,
    column=0,
    padx=10,
    pady=10
)

book_entry = tk.Entry(
    window,
    width=30
)

book_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)


# ================= AUTHOR =================

author_label = tk.Label(
    window,
    text="Author:"
)

author_label.grid(
    row=1,
    column=0,
    padx=10,
    pady=10
)

author_entry = tk.Entry(
    window,
    width=30
)

author_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)


# ================= QUANTITY =================

quantity_label = tk.Label(
    window,
    text="Quantity:"
)

quantity_label.grid(
    row=2,
    column=0,
    padx=10,
    pady=10
)

quantity_entry = tk.Entry(
    window,
    width=30
)

quantity_entry.grid(
    row=2,
    column=1,
    padx=10,
    pady=10
)


# ================= BUTTONS =================

add_button = tk.Button(
    window,
    text="Add Book",
    command=add_book,
    width=15
)

add_button.grid(
    row=4,
    column=0,
    padx=10,
    pady=5
)


search_button = tk.Button(
    window,
    text="Search",
    command=search_book,
    width=15
)

search_button.grid(
    row=4,
    column=1,
    padx=10,
    pady=5
)


update_button = tk.Button(
    window,
    text="Update",
    command=update_book,
    width=15
)

update_button.grid(
    row=5,
    column=0,
    padx=10,
    pady=5
)


delete_button = tk.Button(
    window,
    text="Delete",
    command=delete_book,
    width=15
)

delete_button.grid(
    row=5,
    column=1,
    padx=10,
    pady=5
)


view_button = tk.Button(
    window,
    text="View Books",
    command=view_books,
    width=15
)

view_button.grid(
    row=6,
    column=0,
    padx=10,
    pady=5
)


clear_button = tk.Button(
    window,
    text="Clear",
    command=clear_fields,
    width=15
)

clear_button.grid(
    row=6,
    column=1,
    padx=10,
    pady=5
)


# ================= TABLE =================

table = ttk.Treeview(
    window,
    columns=(
        "ID",
        "Name",
        "Author",
        "Quantity"
    ),
    show="headings"
)

table.heading(
    "ID",
    text="ID"
)

table.heading(
    "Name",
    text="Name"
)

table.heading(
    "Author",
    text="Author"
)

table.heading(
    "Quantity",
    text="Quantity"
)


table.column(
    "ID",
    width=50
)

table.column(
    "Name",
    width=150
)

table.column(
    "Author",
    width=150
)

table.column(
    "Quantity",
    width=80
)


table.grid(
    row=8,
    column=0,
    columnspan=2,
    padx=10,
    pady=20
)


# ================= SELECT TABLE ROW =================

table.bind(
    "<ButtonRelease-1>",
    select_book
)


# ================= DISPLAY BOOKS =================

view_books()


# ================= START APPLICATION =================

window.mainloop()
print("Hi, I am Jai Khape")
print("I am learning Python")