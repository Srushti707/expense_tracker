This project is an **Expense Tracker Application** that allows users to manage their personal finances. It is built using **Python** for the logic, **Tkinter** for the GUI, and **MySQL** for data storage. Users can register, log in, record transactions, and get summarized views of their expenses and income.

### **Key Features**

1. **User Authentication**

   * Users must log in to use the app.
   * New users can register with a unique username and password.

2. **Transaction Management**

   * Users can add transactions categorized as **Income** or **Expense**.
   * Each transaction has an **amount**, **category**, and **date**.
   * Users can **update** or **delete** transactions as needed.
   * Transactions are displayed in a table using Tkinter’s `ttk.Treeview` widget for easy viewing.

3. **Summary Reports**

   * **Monthly Expense Summary**: Shows total expenses for the current month.
   * **Yearly Expense Summary**: Shows total expenses for the past 12 months.
   * **Yearly Income Summary**: Shows total income for the past 12 months.

4. **User-Friendly GUI**

   * Interactive and simple interface.
   * Buttons for actions like Add, Update, Delete, and viewing summaries.
   * Color-coded buttons for clarity.

### **Database Structure**

The app uses **MySQL** with two tables:

1. **Users**

   * `id` (Primary Key)
   * `username` (unique)
   * `password`

2. **Transactions**

   * `id` (Primary Key)
   * `user_id` (links to Users table)
   * `type` (Income or Expense)
   * `amount`
   * `category`
   * `date`

All transactions are linked to a specific user, so multiple users can use the app independently.

### **How It Works**

1. On running the script, the user sees a **login/register screen**.
2. After login, the **main screen** allows the user to:

   * Add a transaction
   * Update/delete selected transactions
   * View summaries
3. Transaction data is stored in the MySQL database, ensuring persistence.
4. Summaries are calculated in real-time from stored transactions.
5. 
### **Use Cases**

* Individuals tracking personal expenses and income.
* Small business owners managing simple cash flow.
* Students monitoring their spending habits.
* 
### **Possible Improvements**

* Add charts and graphs to visualize spending patterns.
* Export reports as CSV or PDF files.
* Add password encryption for better security.
* Enable filtering by category, date, or amount.
