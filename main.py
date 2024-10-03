# main.py

import tkinter as tk
from ui_handler import FinanceTrackerUI
from commands import parse_command
import file_manager
from tkinter import messagebox

def main():
    # Initialize the transactions file
    file_manager.initialize_transactions_file()
    current_id = file_manager.get_id()

    # Initialize the main Tkinter window
    root = tk.Tk()

    # Placeholder for UI reference
    app = None

    def command_callback(user_input):
        """
        Callback function to handle user commands.

        Parameters:
            user_input (str): The command entered by the user.
        """
        command_tuple = parse_command(user_input)
        if not command_tuple:
            return
        
        global current_id

        cmd = command_tuple[0]

        if cmd == 'add':
            _, amount, description, date, category = command_tuple
            file_manager.add_transaction(amount, description, date, category, current_id)
            current_id = current_id + 1
            refresh_ui()
            app.display_message("Success", "Transaction added successfully!")

        elif cmd == 'view':
            refresh_ui()

        elif cmd == 'total':
            transactions = file_manager.read_transactions()
            total_income, total_expenses, net_balance = file_manager.calculate_totals(transactions)
            app.display_message("Totals", f"Total Income: ${total_income:.2f}\n"
                                        f"Total Expenses: ${abs(total_expenses):.2f}\n"
                                        f"Net Balance: ${net_balance:.2f}")

        elif cmd == 'exit':
            root.quit()

    def refresh_ui():
        """
        Refreshes the UI by clearing and repopulating the transaction Treeviews.
        """
        transactions = file_manager.read_transactions()
        app.clear_transactions()

        for txn in transactions:
            try:
                amount = float(txn['Amount'])
                description = txn['Description']
                date = txn['Date']
                category = txn['Category']
                if amount >= 0:
                    app.add_income_transaction(amount, description, date, category)
                else:
                    app.add_expense_transaction(abs(amount), description, date, category)
            except ValueError:
                continue

        total_income, total_expenses, net_balance = file_manager.calculate_totals(transactions)
        app.update_totals(total_income, total_expenses, net_balance)

    # Initialize the UI with the command callback
    app = FinanceTrackerUI(root, command_callback)

    # Initial refresh to display existing transactions
    refresh_ui()

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
