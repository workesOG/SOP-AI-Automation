# ui_handler.py

import tkinter as tk
from tkinter import ttk, messagebox

class FinanceTrackerUI:
    def __init__(self, root, command_callback):
        """
        Initializes the UI components.

        Parameters:
            root (tk.Tk): The root window.
            command_callback (function): The function to call when a command is entered.
        """
        self.root = root
        self.command_callback = command_callback
        self.root.title("Personal Finance Tracker")
        self.root.geometry("800x650")  # Updated height to 650px
        self.create_widgets()

    def create_widgets(self):
        # Frame for Income Transactions
        income_frame = tk.LabelFrame(self.root, text="Income Transactions", padx=10, pady=10)
        income_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Treeview for displaying income transactions
        income_columns = ('Amount', 'Description', 'Date', 'Category')
        self.income_tree = ttk.Treeview(income_frame, columns=income_columns, show='headings', height=10)
        for col in income_columns:
            self.income_tree.heading(col, text=col)
            self.income_tree.column(col, anchor="center", width=150)
        self.income_tree.pack(side='left', fill="both", expand=True)

        # Scrollbar for the Income Treeview
        income_scrollbar = ttk.Scrollbar(income_frame, orient=tk.VERTICAL, command=self.income_tree.yview)
        self.income_tree.configure(yscroll=income_scrollbar.set)
        income_scrollbar.pack(side='right', fill='y')

        # Frame for Expense Transactions
        expense_frame = tk.LabelFrame(self.root, text="Expense Transactions", padx=10, pady=10)
        expense_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Treeview for displaying expense transactions
        expense_columns = ('Amount', 'Description', 'Date', 'Category')
        self.expense_tree = ttk.Treeview(expense_frame, columns=expense_columns, show='headings', height=10)
        for col in expense_columns:
            self.expense_tree.heading(col, text=col)
            self.expense_tree.column(col, anchor="center", width=150)
        self.expense_tree.pack(side='left', fill="both", expand=True)

        # Scrollbar for the Expense Treeview
        expense_scrollbar = ttk.Scrollbar(expense_frame, orient=tk.VERTICAL, command=self.expense_tree.yview)
        self.expense_tree.configure(yscroll=expense_scrollbar.set)
        expense_scrollbar.pack(side='right', fill='y')

        # Frame for totals
        totals_frame = tk.Frame(self.root)
        totals_frame.pack(fill="x", padx=10, pady=5)

        self.income_label = tk.Label(totals_frame, text="Total Income: $0.00", font=("Helvetica", 12))
        self.income_label.pack(side='left', padx=10)

        self.expenses_label = tk.Label(totals_frame, text="Total Expenses: $0.00", font=("Helvetica", 12))
        self.expenses_label.pack(side='left', padx=10)

        self.balance_label = tk.Label(totals_frame, text="Net Balance: $0.00", font=("Helvetica", 12, 'bold'))
        self.balance_label.pack(side='left', padx=10)

        # Frame for command-line
        cmd_frame = tk.Frame(self.root)
        cmd_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(cmd_frame, text="Command:").pack(side='left')
        self.cmd_entry = tk.Entry(cmd_frame, width=80)
        self.cmd_entry.pack(side='left', padx=5)
        self.cmd_entry.bind("<Return>", self.on_enter_command)

    def on_enter_command(self, event):
        """
        Handles the event when the user presses Enter in the command entry.

        Parameters:
            event: The event object.
        """
        user_input = self.cmd_entry.get().strip()
        if not user_input:
            return

        # Clear the command entry
        self.cmd_entry.delete(0, tk.END)

        # Call the command callback with the user input
        self.command_callback(user_input)

    def add_income_transaction(self, amount, description, date, category):
        """
        Adds a transaction to the Income Treeview.

        Parameters:
            amount (float): The amount of the transaction.
            description (str): Description of the transaction.
            date (str): Date of the transaction.
            category (str): Category of the transaction.
        """
        self.income_tree.insert('', tk.END, values=(
            f"${amount:.2f}",
            description,
            date,
            category
        ), tags=('income',))

    def add_expense_transaction(self, amount, description, date, category):
        """
        Adds a transaction to the Expense Treeview.

        Parameters:
            amount (float): The amount of the transaction (positive value).
            description (str): Description of the transaction.
            date (str): Date of the transaction.
            category (str): Category of the transaction.
        """
        self.expense_tree.insert('', tk.END, values=(
            f"${amount:.2f}",
            description,
            date,
            category
        ), tags=('expense',))

    def clear_transactions(self):
        """
        Clears all transactions from both Treeviews.
        """
        for item in self.income_tree.get_children():
            self.income_tree.delete(item)
        for item in self.expense_tree.get_children():
            self.expense_tree.delete(item)

    def update_totals(self, total_income, total_expenses, net_balance):
        """
        Updates the totals labels.

        Parameters:
            total_income (float): The total income.
            total_expenses (float): The total expenses.
            net_balance (float): The net balance.
        """
        self.income_label.config(text=f"Total Income: ${total_income:.2f}")
        self.expenses_label.config(text=f"Total Expenses: ${abs(total_expenses):.2f}")
        self.balance_label.config(text=f"Net Balance: ${net_balance:.2f}")

    def display_message(self, title, message):
        """
        Displays an informational message.

        Parameters:
            title (str): The title of the message box.
            message (str): The message to display.
        """
        messagebox.showinfo(title, message)

    def display_error(self, title, message):
        """
        Displays an error message.

        Parameters:
            title (str): The title of the message box.
            message (str): The error message to display.
        """
        messagebox.showerror(title, message)
