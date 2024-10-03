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
            writer.writerow(['Amount', 'Description', 'Date', 'Category', 'ID'])

def add_transaction(amount, description, date, category, id):
    """
    Adds a new transaction to the CSV file.

    Parameters:
        amount (float): The amount of the transaction (positive for income, negative for expenses).
        description (str): Description of the transaction.
        date (str): Date of the transaction in YYYY-MM-DD format.
        category (str): Category of the transaction.
        id (num): The hidden id
    """
    with open(TRANSACTIONS_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([f"{amount:.2f}", description, date, category, id])

def read_transactions():
    """
    Reads all transactions from the CSV file.

    Returns:
        list of dict: A list of transactions where each transaction is represented as a dictionary.
    """
    with open(TRANSACTIONS_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def get_id():
    transactions = read_transactions()
    highest_id = -1;
    for txn in transactions:
        if txn['ID'] > highest_id:
            highest_id = txn['ID']
            
    return highest_id + 1

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
