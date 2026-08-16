import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox


# ---------------- DATABASE ----------------

def create_database():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ---------------- CLEAR FIELDS ----------------

def clear_fields():
    date_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)


# ---------------- ADD EXPENSE ----------------

def add_expense():

    date = date_entry.get().strip()
    description = description_entry.get().strip()
    category = category_entry.get().strip()
    amount = amount_entry.get().strip()

    if date == "" or description == "" or category == "" or amount == "":
        messagebox.showwarning("Warning", "Please fill all fields.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number.")
        return

    if amount <= 0:
        messagebox.showerror("Error", "Amount must be greater than 0.")
        return

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO expenses(date, description, category, amount)
        VALUES (?, ?, ?, ?)
        """,
        (date, description, category, amount)
    )

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Expense added successfully.")

    clear_fields()
    view_expense()


# ---------------- VIEW EXPENSES ----------------

def view_expense():

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses ORDER BY id DESC")
    expenses = cursor.fetchall()

    conn.close()

    for row in table.get_children():
        table.delete(row)

    for expense in expenses:
        table.insert("", tk.END, values=expense)

    update_total()


# ---------------- SEARCH EXPENSE ----------------

def search_expense():

    search = search_entry.get().strip()

    if search == "":
        view_expense()
        return

    search_value = f"%{search}%"

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM expenses
        WHERE description LIKE ?
        OR category LIKE ?
        OR date LIKE ?
        """,
        (search_value, search_value, search_value)
    )

    expenses = cursor.fetchall()
    conn.close()

    for row in table.get_children():
        table.delete(row)

    for expense in expenses:
        table.insert("", tk.END, values=expense)


# ---------------- DELETE EXPENSE ----------------

def delete_expense():

    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select an expense from the table."
        )
        return

    item = table.item(selected[0])
    expense_id = item["values"][0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this expense?"
    )

    if not confirm:
        return

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Expense deleted successfully.")

    clear_fields()
    view_expense()


# ---------------- SELECT EXPENSE ----------------

def select_expense(event):

    selected = table.selection()

    if not selected:
        return

    item = table.item(selected[0])
    values = item["values"]

    clear_fields()

    date_entry.insert(0, values[1])
    description_entry.insert(0, values[2])
    category_entry.insert(0, values[3])
    amount_entry.insert(0, values[4])


# ---------------- UPDATE EXPENSE ----------------

def update_expense():

    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select an expense from the table."
        )
        return

    item = table.item(selected[0])
    expense_id = item["values"][0]

    date = date_entry.get().strip()
    description = description_entry.get().strip()
    category = category_entry.get().strip()
    amount = amount_entry.get().strip()

    if date == "" or description == "" or category == "" or amount == "":
        messagebox.showwarning(
            "Warning",
            "Please fill all fields."
        )
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Amount must be a number."
        )
        return

    if amount <= 0:
        messagebox.showerror(
            "Error",
            "Amount must be greater than 0."
        )
        return

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE expenses
        SET date = ?, description = ?, category = ?, amount = ?
        WHERE id = ?
        """,
        (date, description, category, amount, expense_id)
    )

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        "Expense updated successfully."
    )

    clear_fields()
    view_expense()


# ---------------- TOTAL EXPENSES ----------------

def update_total():

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM expenses")

    result = cursor.fetchone()

    conn.close()

    total = result[0] if result[0] is not None else 0

    total_label.config(
        text=f"Total Expenses: ₹{total:.2f}"
    )


# ---------------- MAIN WINDOW ----------------

create_database()

window = tk.Tk()
window.title("Expense Tracker")
window.geometry("850x650")
window.resizable(False, False)


# ---------------- TITLE ----------------

title_label = tk.Label(
    window,
    text="Expense Tracker",
    font=("Arial", 22, "bold")
)

title_label.grid(
    row=0,
    column=0,
    columnspan=4,
    pady=15
)


# ---------------- LABELS ----------------

tk.Label(
    window,
    text="Date:"
).grid(row=1, column=0, padx=10, pady=8)

tk.Label(
    window,
    text="Description:"
).grid(row=2, column=0, padx=10, pady=8)

tk.Label(
    window,
    text="Category:"
).grid(row=3, column=0, padx=10, pady=8)

tk.Label(
    window,
    text="Amount:"
).grid(row=4, column=0, padx=10, pady=8)


# ---------------- ENTRY FIELDS ----------------

date_entry = tk.Entry(
    window,
    width=30
)
date_entry.grid(row=1, column=1, padx=10, pady=8)

description_entry = tk.Entry(
    window,
    width=30
)
description_entry.grid(row=2, column=1, padx=10, pady=8)

category_entry = tk.Entry(
    window,
    width=30
)
category_entry.grid(row=3, column=1, padx=10, pady=8)

amount_entry = tk.Entry(
    window,
    width=30
)
amount_entry.grid(row=4, column=1, padx=10, pady=8)


# ---------------- BUTTONS ----------------

add_button = tk.Button(
    window,
    text="Add Expense",
    command=add_expense,
    width=15
)
add_button.grid(row=5, column=0, padx=10, pady=8)

update_button = tk.Button(
    window,
    text="Update",
    command=update_expense,
    width=15
)
update_button.grid(row=5, column=1, padx=10, pady=8)

delete_button = tk.Button(
    window,
    text="Delete",
    command=delete_expense,
    width=15
)
delete_button.grid(row=5, column=2, padx=10, pady=8)

clear_button = tk.Button(
    window,
    text="Clear",
    command=clear_fields,
    width=15
)
clear_button.grid(row=5, column=3, padx=10, pady=8)


# ---------------- SEARCH ----------------

tk.Label(
    window,
    text="Search:"
).grid(row=6, column=0, padx=10, pady=8)

search_entry = tk.Entry(
    window,
    width=30
)
search_entry.grid(row=6, column=1, padx=10, pady=8)

search_button = tk.Button(
    window,
    text="Search",
    command=search_expense,
    width=15
)
search_button.grid(row=6, column=2, padx=10, pady=8)

view_button = tk.Button(
    window,
    text="View All",
    command=view_expense,
    width=15
)
view_button.grid(row=6, column=3, padx=10, pady=8)


# ---------------- TOTAL ----------------

total_label = tk.Label(
    window,
    text="Total Expenses: ₹0.00",
    font=("Arial", 14, "bold")
)

total_label.grid(
    row=7,
    column=0,
    columnspan=4,
    pady=10
)


# ---------------- TABLE ----------------

table_frame = tk.Frame(window)

table_frame.grid(
    row=8,
    column=0,
    columnspan=4,
    padx=10,
    pady=10
)

table = ttk.Treeview(
    table_frame,
    columns=(
        "ID",
        "Date",
        "Description",
        "Category",
        "Amount"
    ),
    show="headings",
    height=12
)

table.heading("ID", text="ID")
table.heading("Date", text="Date")
table.heading("Description", text="Description")
table.heading("Category", text="Category")
table.heading("Amount", text="Amount")

table.column("ID", width=50)
table.column("Date", width=100)
table.column("Description", width=180)
table.column("Category", width=120)
table.column("Amount", width=100)


# ---------------- SCROLLBAR ----------------

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=table.yview
)

table.configure(
    yscrollcommand=scrollbar.set
)

table.grid(row=0, column=0)

scrollbar.grid(
    row=0,
    column=1,
    sticky="ns"
)


# ---------------- TABLE CLICK ----------------

table.bind(
    "<ButtonRelease-1>",
    select_expense
)


# ---------------- START ----------------

view_expense()

window.mainloop()