# file_manager.py

import csv
import os
from datetime import datetime

# File where transactions will be stored
TRANSACTIONS_FILE = 'transactions.csv'

def initialize_transactions_file():
    """
    Initializes the transactions CSV file with headers if it doesn't exist.
    """
    if not os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Amount', 'Description', 'Date', 'Category', "ID"])

def generate_unique_id():
    """
    Generates a unique ID based on the highest existing ID in the file.

    Returns:
        int: The next unique ID.
    """
    transactions = read_transactions()
    if not transactions:
        return 0
    return max(int(txn['ID']) for txn in transactions) + 1

def add_transaction(amount, description, date, category):
    """
    Adds a new transaction to the CSV file.

    Parameters:
        amount (float): The amount of the transaction (positive for income, negative for expenses).
        description (str): Description of the transaction.
        date (str): Date of the transaction in YYYY-MM-DD format.
        category (str): Category of the transaction.
    """
    unique_id = generate_unique_id()
    with open(TRANSACTIONS_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([f"{amount:.2f}", description, date, category, unique_id])

def read_transactions():
    """
    Reads all transactions from the CSV file.

    Returns:
        list of dict: A list of transactions where each transaction is represented as a dictionary.
    """
    with open(TRANSACTIONS_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def edit_transaction(transaction_id, field, new_value):
    """
    Edits a specific field of a transaction based on its unique ID.

    Parameters:
        transaction_id (int): The ID of the transaction to edit.
        field (str): The field to edit ('amount', 'description', 'date', 'category').
        new_value: The new value for the field.

    Returns:
        bool: True if the transaction was edited, False otherwise.
    """
    transactions = read_transactions()
    edited = False

    for txn in transactions:
        if int(txn['ID']) == transaction_id:
            # Update the field
            if field == 'amount':
                txn['Amount'] = f"{float(new_value):.2f}"
            elif field == 'description':
                txn['Description'] = new_value
            elif field == 'date':
                # Validate and format the date
                try:
                    day, month, year = map(int, new_value.split('/'))
                    txn['Date'] = f"{year:04d}/{month:02d}/{day:02d}"
                except ValueError:
                    return False
            elif field == 'category':
                txn['Category'] = new_value

            edited = True
            break

    if edited:
        # Rewrite the CSV file with the updated transactions
        with open(TRANSACTIONS_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Amount', 'Description', 'Date', 'Category', 'ID'])
            writer.writeheader()
            writer.writerows(transactions)
        return True

    return False


def calculate_totals(transactions):
    """
    Calculates total income, total expenses, and net balance.

    Parameters:
        transactions (list of dict): The list of transactions.

    Returns:
        tuple: Total income, total expenses, and net balance.
    """
    total_income = 0.0
    total_expenses = 0.0
    for txn in transactions:
        try:
            amount = float(txn['Amount'])
            if amount >= 0:
                total_income += amount
            else:
                total_expenses += amount
        except (KeyError, ValueError):
            continue
    net_balance = total_income + total_expenses
    return total_income, total_expenses, net_balance

def renumber_ids():
    """
    Renumbers the IDs of all transactions sequentially, starting from 0.

    This function ensures that IDs are always in sequential order after any modification,
    such as removing transactions.

    Returns:
        None
    """
    transactions = read_transactions()

    # Assign new sequential IDs
    for index, txn in enumerate(transactions):
        txn['ID'] = str(index)

    # Rewrite the CSV file with updated IDs
    with open(TRANSACTIONS_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Amount', 'Description', 'Date', 'Category', 'ID'])
        writer.writeheader()
        writer.writerows(transactions)

def remove_transaction_by_id(transaction_id):
    """
    Removes a transaction based on its unique ID.

    Parameters:
        transaction_id (int): The ID of the transaction to remove.

    Returns:
        bool: True if a transaction was removed, False otherwise.
    """
    transactions = read_transactions()
    filtered_transactions = [txn for txn in transactions if int(txn['ID']) != transaction_id]

    if len(filtered_transactions) == len(transactions):
        # No transaction was removed
        return False

    # Rewrite the CSV file with the updated list
    with open(TRANSACTIONS_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Amount', 'Description', 'Date', 'Category', 'ID'])
        writer.writeheader()
        writer.writerows(filtered_transactions)
    return True