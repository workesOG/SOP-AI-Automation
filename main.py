# main.py

import tkinter as tk
from ui_handler import FinanceTrackerUI
from commands import parse_command
import file_manager
import categories_manager
from ai_handler import translate_natural_language_to_commands
from tkinter import messagebox

def main():
    # Initialize the transactions file
    file_manager.initialize_transactions_file()
    categories_manager.initialize_categories_file()

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
        # First, attempt to parse the command normally
        command_tuple = parse_command(user_input)
        
        if not command_tuple:
            # If parsing fails, attempt to use AI to interpret the command
            command_sequence = translate_natural_language_to_commands(user_input)
            
            if not command_sequence:
                # If AI also fails, notify the user
                app.display_error("Command Error", "Unable to parse the command. Please try again.")
                return

            # Ensure that command_sequence is an instance of CommandSequence
            if isinstance(command_sequence, tuple):
                # Single command returned as a tuple
                commands = [command_sequence]
            elif isinstance(command_sequence, list):
                # List of Command objects
                commands = command_sequence
            else:
                # Unsupported format
                app.display_error("Command Error", "AI returned an unsupported command format.")
                return
        else:
            # Single command parsed normally
            commands = [command_tuple]

        # Eaxecute each commnd in the sequence
        for cmd in commands:
            execute_individual_command(cmd, app)

    def ai_commands_callback(user_input):
        command_sequence = translate_natural_language_to_commands(user_input)
        for command in command_sequence:
            #command_to_execute = f"{command.command} {command.amount} \"{command.description}\" {command.date} \"{command.category}\""
            print(command)
            execute_individual_command(command, app)  # Pass the app reference

    def execute_individual_command(command, app):
        """
        Executes an individual command.

        Parameters:
        command (Command): The command object containing all arguments.
        app (FinanceTrackerUI): Reference to the app UI for displaying messages and errors.
        """
        cmd = command.command  # Extract the command name

        if cmd == 'add':
            if not (command.amount and command.description and command.date and command.category):
                app.display_error("Command Error", "Missing arguments for 'add' command.")
                return

            # Convert DD/MM/YYYY to YYYY-MM-DD
            try:
                day, month, year = map(int, command.date.split('/'))
                formatted_date = f"{year:04d}-{month:02d}-{day:02d}"
            except ValueError:
                app.display_error("Date Error", f"Invalid date format: {command.date}. Expected DD/MM/YYYY.")
                return

            # Add the transaction
            file_manager.add_transaction(command.amount, command.description, formatted_date, command.category)
            refresh_ui()
            app.display_message(
                "Success",
                f"Transaction added successfully!\nDescription: {command.description}\nAmount: ${command.amount:.2f}\n"
                f"Date: {formatted_date}\nCategory: {command.category}"
            )

        elif cmd == 'category':
            if not (command.action):
                app.display_error("Command Error", "Missing arguments for 'category' command.")
                return
            if not (command.name):
                if command.action == "reset":
                    categories_manager.reset_to_default_categories()
                    app.display_message("Success", f"Categories reset to default!")
                    return
                else:
                    app.display_error("Command Error", "Missing arguments for 'category' command.")
                    return
            if command.action == "add":
                categories_manager.add_category(command.name)
                app.display_message(
                "Success",
                f"Category added successfully!\nName: {command.name}"
            )
            else:
                success = categories_manager.remove_category(command.name)
                if success:
                    app.display_message(
                    "Success",
                    f"Category removed successfully!\nName: {command.name}"
                    )
                else:
                    app.display_message(
                    "Unsuccessful",
                    f"Category not found: {command.name}"
                    )

        elif cmd == 'remove':
            if not command.unique_ids or len(command.unique_ids) == 0:
                app.display_error("Command Error", "No IDs provided for 'remove' command.")
                return

            unsuccessful_ids = []
            for unique_id in command.unique_ids:
                if unique_id < 0:
                    app.display_error("Command Error", f"Invalid ID: {unique_id}. IDs must be non-negative.")
                    unsuccessful_ids.append(unique_id)
                    continue

                success = file_manager.remove_transaction_by_id(unique_id)
                if not success:
                    unsuccessful_ids.append(unique_id)

            if not unsuccessful_ids:
                app.display_message(
                    "Success",
                    f"Transactions removed successfully! IDs: {', '.join(map(str, command.unique_ids))}"
                )
            else:
                app.display_message(
                    "Partial Success",
                    f"Some transactions could not be found: {', '.join(map(str, unsuccessful_ids))}"
                )
            file_manager.renumber_ids()
            refresh_ui()
        
        elif cmd == 'edit':
            if not command.unique_ids or len(command.unique_ids) != 1:
                app.display_error("Command Error", "Provide exactly one ID for 'edit' command.")
                return

            unique_id = command.unique_ids[0]
            field = command.field
            new_value = command.value

            # Attempt to edit the transaction
            success = file_manager.edit_transaction(unique_id, field, new_value)

            if success:
                app.display_message("Success", f"Transaction {unique_id} updated successfully!")
                file_manager.renumber_ids()
                refresh_ui()
            else:
                app.display_error("Transaction Error", f"Transaction with ID {unique_id} could not be found.")


        else:
            app.display_error("Command Error", f"Unknown command: {cmd}")

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
                date_str = txn['Date']
                category = txn['Category']
                if amount >= 0:
                    app.add_income_transaction(amount, description, date_str, category)
                else:
                    app.add_expense_transaction(abs(amount), description, date_str, category)
            except ValueError:
                continue

        total_income, total_expenses, net_balance = file_manager.calculate_totals(transactions)
        app.update_totals(total_income, total_expenses, net_balance)

    # Initialize the UI with the command callback
    app = FinanceTrackerUI(root, command_callback, ai_commands_callback)

    # Initial refresh to display existing transactions
    refresh_ui()

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
