import os

# File path for the categories file
CATEGORIES_FILE = 'categories.txt'

# Default categories
DEFAULT_CATEGORIES = [
    "Groceries",
    "Rent",
    "Utilities",
    "Transportation",
    "Entertainment",
    "Dining",
    "Savings",
    "Investments",
    "Medical",
    "Miscellaneous"
]

def initialize_categories_file():
    """
    Ensures the categories file exists and is correctly formatted.
    If the file doesn't exist or is improperly formatted, resets it to default categories.
    """
    if not os.path.exists(CATEGORIES_FILE):
        # Create the file with default categories if it doesn't exist
        reset_to_default_categories()
        return

    # Validate the existing file
    if not validate_categories_file():
        # Reset the file to default categories if invalid
        reset_to_default_categories()

def reset_to_default_categories():
    """
    Resets the categories file to the default categories.
    """
    with open(CATEGORIES_FILE, mode='w') as file:
        for category in DEFAULT_CATEGORIES:
            file.write(category + '\n')

def validate_categories_file():
    """
    Validates the categories file to ensure it is correctly formatted.

    Returns:
        bool: True if the file is valid, False otherwise.
    """
    try:
        with open(CATEGORIES_FILE, mode='r') as file:
            lines = file.readlines()

        # Ensure all lines are non-empty and have no extra spaces
        for line in lines:
            stripped_line = line.strip()
            if not stripped_line:  # Empty line
                return False
            if '\n' in stripped_line:  # Multi-line content in one line
                return False

        return True
    except Exception as e:
        print(f"Error validating categories file: {e}")
        return False

def read_categories():
    """
    Reads the categories from the file.

    Returns:
        list: A list of categories.
    """
    with open(CATEGORIES_FILE, mode='r') as file:
        return [line.strip() for line in file.readlines()]

def add_category(category):
    """
    Adds a new category to the file if it doesn't already exist.

    Parameters:
        category (str): The category to add.
    """
    categories = read_categories()
    if category not in categories:
        with open(CATEGORIES_FILE, mode='a') as file:
            file.write('\n' + category)

def remove_category(category):
    """
    Removes a category from the file if it exists.

    Parameters:
        category (str): The category to remove.
    """
    categories = read_categories()
    if category in categories:
        categories.remove(category)
        with open(CATEGORIES_FILE, mode='w') as file:
            for cat in categories:
                file.write(cat + '\n')
        return True
    else:
        return False
