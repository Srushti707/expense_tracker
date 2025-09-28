import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from datetime import datetime, timedelta
try:
    temp_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="toor"
    )
    temp_cursor = temp_conn.cursor()
    temp_cursor.execute("CREATE DATABASE IF NOT EXISTS ExpenseTracker")
    temp_conn.commit()
    temp_cursor.close()
    temp_conn.close()
except mysql.connector.Error as err:
    messagebox.showerror("Database Error", f"Failed to connect or create DB: {err}")

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="toor",
        database="ExpenseTracker"
    )
    cursor = conn.cursor()
except mysql.connector.Error as err:
    messagebox.showerror("Database Error", f"Could not connect to ExpenseTracker DB: {err}")

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    type VARCHAR(10),
    amount DECIMAL(10,2),
    category VARCHAR(50),
    date DATE,
    FOREIGN KEY (user_id) REFERENCES Users(id)
)
''')

conn.commit()

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.user_id = None
        self.root.configure(bg="#f0f4f7")
        self.build_login_screen()

    def build_login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Login to Expense Tracker", font=("Arial", 16, "bold"), bg="#f0f4f7", fg="#333").pack(pady=10)

        tk.Label(self.root, text="Username:", bg="#f0f4f7").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:", bg="#f0f4f7").pack()
        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", command=self.login, bg="#4caf50", fg="white", width=15).pack(pady=10)
        tk.Button(self.root, text="Register", command=self.register, bg="#2196f3", fg="white", width=15).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        cursor.execute("SELECT id FROM Users WHERE username=%s AND password=%s", (username, password))
        result = cursor.fetchone()
        if result:
            self.user_id = result[0]
            self.build_main_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            cursor.execute("INSERT INTO Users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Registered Successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Could not register: {err}")

    def build_main_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Add Transaction", font=("Arial", 16, "bold"), bg="#f0f4f7", fg="#333").pack(pady=10)

        tk.Label(self.root, text="Type:", bg="#f0f4f7").pack()
        self.type_var = tk.StringVar()
        self.type_dropdown = ttk.Combobox(self.root, textvariable=self.type_var, values=["Income", "Expense"])
        self.type_dropdown.pack(pady=5)

        tk.Label(self.root, text="Amount:", bg="#f0f4f7").pack()
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack(pady=5)

        tk.Label(self.root, text="Category:", bg="#f0f4f7").pack()
        self.category_entry = tk.Entry(self.root)
        self.category_entry.pack(pady=5)

        tk.Label(self.root, text="Date (YYYY-MM-DD):", bg="#f0f4f7").pack()
        self.date_entry = tk.Entry(self.root)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.date_entry.pack(pady=5)

        tk.Button(self.root, text="Add Transaction", command=self.add_transaction, bg="#4caf50", fg="white", width=18).pack(pady=5)
        tk.Button(self.root, text="Monthly Summary", command=self.show_monthly_summary, bg="#ff9800", fg="white", width=18).pack(pady=5)
        tk.Button(self.root, text="Yearly Expense", command=self.show_yearly_expense_summary, bg="#9c27b0", fg="white", width=18).pack(pady=5)
        tk.Button(self.root, text="Yearly Income", command=self.show_yearly_income_summary, bg="#3f51b5", fg="white", width=18).pack(pady=5)

        self.transaction_tree = ttk.Treeview(self.root, columns=("ID", "Type", "Amount", "Category", "Date"), show='headings')
        for col in self.transaction_tree["columns"]:
            self.transaction_tree.heading(col, text=col)
        self.transaction_tree.pack(fill=tk.BOTH, expand=True, pady=10)

        tk.Button(self.root, text="Delete Selected", command=self.delete_transaction, bg="#f44336", fg="white", width=18).pack(pady=5)
        tk.Button(self.root, text="Update Selected", command=self.update_transaction, bg="#607d8b", fg="white", width=18).pack(pady=5)
        tk.Button(self.root, text="Back to Login", command=self.build_login_screen, bg="#9e9e9e", fg="white", width=18).pack(pady=10)

        self.show_transactions()
        self.transaction_tree.bind("<ButtonRelease-1>", self.populate_fields)

    def add_transaction(self):
        type_ = self.type_var.get()
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        date = self.date_entry.get()

        if not all([type_, amount, category, date]):
            messagebox.showerror("Error", "All fields are required")
            return

        cursor.execute('''
            INSERT INTO Transactions (user_id, type, amount, category, date)
            VALUES (%s, %s, %s, %s, %s)
        ''', (self.user_id, type_, amount, category, date))
        conn.commit()
        messagebox.showinfo("Added", "Transaction Added")
        self.show_transactions()

    def show_transactions(self):
        self.transaction_tree.delete(*self.transaction_tree.get_children())
        cursor.execute("SELECT id, type, amount, category, date FROM Transactions WHERE user_id=%s", (self.user_id,))
        for row in cursor.fetchall():
            self.transaction_tree.insert('', tk.END, values=row)

    def delete_transaction(self):
        selected = self.transaction_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No transaction selected")
            return
        transaction_id = self.transaction_tree.item(selected[0])['values'][0]
        cursor.execute("DELETE FROM Transactions WHERE id=%s", (transaction_id,))
        conn.commit()
        self.show_transactions()
        messagebox.showinfo("Deleted", "Transaction deleted")

    def update_transaction(self):
        selected = self.transaction_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No transaction selected to update")
            return

        transaction_id = self.transaction_tree.item(selected[0])['values'][0]
        type_ = self.type_var.get()
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        date = self.date_entry.get()

        if not all([type_, amount, category, date]):
            messagebox.showerror("Error", "All fields are required")
            return

        cursor.execute('''
            UPDATE Transactions
            SET type=%s, amount=%s, category=%s, date=%s
            WHERE id=%s AND user_id=%s
        ''', (type_, amount, category, date, transaction_id, self.user_id))
        conn.commit()
        self.show_transactions()
        messagebox.showinfo("Updated", "Transaction updated successfully")

    def populate_fields(self, event):
        selected = self.transaction_tree.selection()
        if not selected:
            return
        data = self.transaction_tree.item(selected[0], "values")
        self.type_var.set(data[1])
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, data[2])
        self.category_entry.delete(0, tk.END)
        self.category_entry.insert(0, data[3])
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, data[4])

    def show_monthly_summary(self):
        now = datetime.now()
        cursor.execute('''
            SELECT SUM(amount) FROM Transactions
            WHERE user_id = %s AND type = 'Expense'
            AND MONTH(date) = %s AND YEAR(date) = %s
        ''', (self.user_id, now.month, now.year))
        result = cursor.fetchone()
        total = result[0] if result[0] else 0
        messagebox.showinfo("Monthly Expense", f"Total expenses this month: ₹{total:.2f}")

    def show_yearly_expense_summary(self):
        today = datetime.now()
        past_year = today - timedelta(days=365)
        cursor.execute('''
            SELECT SUM(amount) FROM Transactions
            WHERE user_id = %s AND type = 'Expense'
            AND date BETWEEN %s AND %s
        ''', (self.user_id, past_year.date(), today.date()))
        result = cursor.fetchone()
        total = result[0] if result[0] else 0
        messagebox.showinfo("Yearly Expense", f"Total expenses in last 12 months: ₹{total:.2f}")

    def show_yearly_income_summary(self):
        today = datetime.now()
        past_year = today - timedelta(days=365)
        cursor.execute('''
            SELECT SUM(amount) FROM Transactions
            WHERE user_id = %s AND type = 'Income'
            AND date BETWEEN %s AND %s
        ''', (self.user_id, past_year.date(), today.date()))
        result = cursor.fetchone()
        total = result[0] if result[0] else 0
        messagebox.showinfo("Yearly Income", f"Total income in last 12 months: ₹{total:.2f}")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("700x600")
    root.configure(bg="#f0f4f7")
    app = ExpenseApp(root)
    root.mainloop()
