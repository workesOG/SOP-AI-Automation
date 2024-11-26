import shlex
from datetime import datetime
from tkinter import messagebox
from ai_handler import Command

def parse_command(input_str):
    """
    Parses the user input and returns a Command object.

    Parameters:
        input_str (str): The command input by the user.

    Returns:
        Command or None: A Command object representing the parsed command, or None if invalid.
    """
    try:
        tokens = shlex.split(input_str)
    except ValueError as e:
        messagebox.showerror("Command Error", f"Invalid command syntax: {e}")
        return None

    if not tokens:
        return None

    cmd = tokens[0].lower()

    if cmd == 'add':
        if len(tokens) < 5:
            messagebox.showerror("Command Error", 'Usage: add <amount> "<description>" <date DD/MM/YYYY> "<category>"')
            return None
        try:
            amount = float(tokens[1])
        except ValueError:
            messagebox.showerror("Command Error", "Amount must be a number.")
            return None
        description = tokens[2]
        date = tokens[3]
        category = tokens[4]
        # Validate date format
        try:
            datetime.strptime(date, '%d/%m/%Y')
        except ValueError:
            messagebox.showerror("Command Error", "Date must be in DD/MM/YYYY format.")
            return None
        return Command(command='add', amount=amount, description=description, date=date, category=category)

    elif cmd == 'category':
        if len(tokens) < 2:
            messagebox.showerror("Command Error", 'Usage: category <add / remove / reset> "<name>"')
            return None

        action = tokens[1].lower()
        if action not in ['add', 'remove', 'reset']:
            messagebox.showerror("Command Error", 'Usage: category <add / remove / reset> "<name>"')
            return None

        if action == 'reset':
            return Command(command='category', action='reset')

        if len(tokens) < 3:
            messagebox.showerror("Command Error", 'Usage: category <add / remove / reset> "<name>"')
            return None

        name = tokens[2]
        return Command(command='category', action=action, name=name)

    elif cmd == 'remove':
        if len(tokens) < 2:
            messagebox.showerror("Command Error", 'Usage: remove <ID> [<ID> ...]')
            return None
        try:
            unique_ids = [int(token) for token in tokens[1:]]
        except ValueError:
            messagebox.showerror("Command Error", "IDs must be integers.")
            return None
        return Command(command='remove', unique_ids=unique_ids)

    elif cmd == 'edit':
        if len(tokens) < 4:
            messagebox.showerror("Command Error", 'Usage: edit <ID> <field> <new value>')
            return None

        try:
            unique_id = int(tokens[1])
        except ValueError:
            messagebox.showerror("Command Error", "ID must be an integer.")
            return None

        field = tokens[2].lower()
        new_value = " ".join(tokens[3:])

        if field not in ['amount', 'description', 'date', 'category']:
            messagebox.showerror("Command Error", f"Invalid field: {field}. Valid fields are amount, description, date, category.")
            return None

        # Convert amount to float if the field is amount
        if field == 'amount':
            try:
                new_value = float(new_value)
            except ValueError:
                messagebox.showerror("Command Error", "Amount must be a number.")
                return None

        return Command(command='edit', unique_ids=[unique_id], name=field, description=new_value)

    else:
        messagebox.showerror("Command Error", f"Unknown command: {cmd}")
        return None
