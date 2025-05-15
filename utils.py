import os

# Function to clear the console screen
def clear_console():
    if os.name == 'nt':  # for Windows
        os.system('cls')

# Any other general utility functions, like input validation or formatting
def format_account_balance(balance):
    return f"${balance:,.2f}"

