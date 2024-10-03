# commands.py

import shlex
from datetime import datetime
from tkinter import messagebox

def parse_command(input_str):
    """
    Parses the user input and returns a tuple representing the command and its arguments.
    Supported commands:
        - add <amount> "<description>" <date DD-MM-YYYY> "<category>"
        - view
        - total
        - exit

    Parameters:
        input_str (str): The command input by the user.

    Returns:
        tuple or None: A tuple containing the command and its arguments, or None if invalid.
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
            messagebox.showerror("Command Error", 'Usage: add <amount> "<description>" <date  DD-MM-YYYY> "<category>"')
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
            datetime.strptime(date, '%d-%m-%Y')
        except ValueError:
            messagebox.showerror("Command Error", "Date must be in  DD-MM-YYYY format.")
            return None
        return ('add', amount, description, date, category)
    
    elif cmd == 'remove':
        return

    elif cmd == 'view':
        return ('view',)

    elif cmd == 'total':
        return ('total',)

    elif cmd == 'exit':
        return ('exit',)

    else:
        messagebox.showerror("Command Error", f"Unknown command: {cmd}")
        return None
