import os
import openai
import json
import categories_manager
import file_manager
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional, List
from datetime import date

# Load environment variables
load_dotenv()

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
openai.api_key = OPENAI_API_KEY

# Define Command Model
class Command(BaseModel):
    command: str
    name: Optional[str] = None
    amount: Optional[float] = None
    value: Optional[str] = None
    description: Optional[str] = None
    date: Optional[str] = None  # DD/MM/YYYY
    action: Optional[str] = None
    category: Optional[str] = None
    field: Optional[str] = None
    unique_ids: Optional[list[int]] = None  # Supports multiple IDs

# Define Command Sequence Model
class CommandSequence(BaseModel):
    commands: List[Command]

# AI Prompt Components
def build_system_prompt():
    """
    Builds the system-level instructions for the AI.

    Returns:
        str: The system prompt.
    """
    return """
    You are a command parser for a Personal Finance Tracker application. Convert the following natural language input into a structured JSON with a series of commands to achieve the desired result.

    Guidelines:
    - Output date in the format: DD/MM/YYYY.
    - If a date is not specified in the user input, assume the current date.
    - Transactions must include valid descriptions and categories. If no suitable category exists, choose the best fit from available categories.
    - Use uppercase for the first letter of both descriptions and categories.
    - Be careful when you interpret expenses and income, as they use the same command. If the user says they have spent x amount, but they also go paid x amount, you have 1 expense and one income.
    - Having used money is always an expense (negative number), having earned money is always an income (positive number).
    - The command syntaxes are strict unless otherwise stated. If a command can only take one argument, that being an ID, no other arguments are going to work for it.
    - There is a list of defined Categories to be used. ONLY these categories can be used.
    - If the user every asks for a transaction to be in any way modified ("Change", "Edit", "Modify") that is never the add or remove command, always the edit command
    - Only use the "amount" field when it is 100 percent certain to be a number. For example, if doing an edit, dont use amount, as the field you are editing may be a description, and as such not a number.
    - Accurately interpret complex inputs involving multiple transactions.

    Example 1:
    User: I spent 200$ on groceries, 70$ in Walmart, and 130$ in Costco.
    Result: Two transactions:
        1. 70$ in Walmart (Groceries category)
        2. 130$ in Costco (Groceries category)
    Notice that no single 200$ expense was added
    
    Example 2:
    User: I spent 500$ on three things, a new monitor, a new mouse and a new keyboard. The all cost the same
    Result: 3 transactions:
        1. 166.66$ on monitor (Entertainment)
        1. 166.66$ on mouse (Entertainment)
        1. 166.66$ on keyboard (Entertainment)
    Notice that the user said they spent 500$ total, and they cost the same, therefore each item cost 500/3 = ~166.66
    """

def build_information_prompt():
    """
    Builds the dynamic context for the AI, including today's date, available categories, and current transactions.

    Returns:
        str: The dynamic information prompt.
    """
    # Today's date
    today = date.today().strftime("%d/%m/%Y")
    
    # Available categories
    categories = categories_manager.read_categories()
    
    # Current transactions
    transactions = file_manager.read_transactions()
    transaction_list = "\n".join(str(t) for t in transactions)

    return f"""
    Context:
    - Today's date: {today}
    - Available categories: {categories}
    - List of current transactions:
    {transaction_list}
    """

def build_commands_prompt():
    """
    Builds the prompt defining supported commands.

    Returns:
        str: The commands prompt.
    """
    return """
    Supported Commands:

    1. **add**:
        - Syntax: add <amount> <description> <date DD/MM/YYYY> <category>
        - Adds a transaction entry, either an income or an expense depending on amount.
        - Parameters:
            - amount: The transaction amount (positive for income, negative for expense).
            - description: A short description of the transaction.
            - date: The transaction date.
            - category: The category of the transaction (e.g., Groceries, Transport).
        - Notes: Remember to ONLY use the categories you have been informed are valid. Don't make up any categories on your own.

    2. **category**:
        - Syntax: category <action> <name>
        - Manages categories.
        - Parameters:
            - action: One of "add", "remove", or "reset". (put this in the "action" field in the object)
            - name: The name of the category to add or remove (not required for "reset") (Make sure to place this in the "name" field in the object).

    3. **remove**:
        - Syntax: remove <ID> [<ID> ...]
        - Removes one or more transactions by their unique IDs.
        - Parameters:
            - ID: One or more transaction IDs to remove (space-separated for multiple IDs).
            
    4. **edit**:
        - Syntax: edit <ID> <field> <new value>
        - Edits a specific field of a transaction.
        - Parameters:
            - ID: The ID of the transaction to edit. (use the unique_id field)
            - field: The field to edit ('amount', 'description', 'date', 'category'). (Use the field field)
            - new value: The new value to assign to the field. (Use the value field)
        - Notes: Output date in the format: DD/MM/YYYY.
        
        Note on commands: IT IS VERY IMPORTANT THAT ONLY THE PARAMETERS LISTED ARE USED, AND THAT THEY ARE IN THE RIGHT PLACES. DON'T USE ANY FIELDS IN THE JSON OUTPUT THAT YOU HAVE NOT BEEN ASKED TO

    """

def translate_natural_language_to_commands(user_input):
    """
    Translates natural language input into structured commands.

    Parameters:
        user_input (str): The natural language command entered by the user.

    Returns:
        List[Command] or None: A list of parsed Command objects, or None if parsing fails.
    """
    # Build AI prompts
    system_prompt = build_system_prompt()
    information_prompt = build_information_prompt()
    commands_prompt = build_commands_prompt()

    # Send the prompts to the AI
    try:
        response = openai.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "system", "content": information_prompt},
                {"role": "system", "content": commands_prompt},
                {"role": "user", "content": user_input},
            ],
            response_format=CommandSequence,
        )

        # Extract and return the parsed CommandSequence
        return response.choices[0].message.parsed.commands

    except Exception as e:
        print(f"Error in AI handler: {e}")
        return None
