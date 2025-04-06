from account import handle_account_option
from utils import clear_console
class User:
    def __init__(self):
        self.username = ''
        self.pin = ''
    id: int
    username: str
    pin: str

class UserService:
    current_user:User | None = None

    def login(self):
        input('TODO:Login user with ID/name and PIN')
        
    def register(self):
        input('TODO:collect user credentials and save')
        self.current_user = User() #replace this code
    
    def change_pin(self):
        input("TODO: Change PIN")
    # Other methods here

user_service = UserService()

EXIT, LOGIN, REGISTER = (0, 1, 2)
def print_main_menu():
    print("Options:")
    print(f"\t{LOGIN} : Login")
    print(f"\t{REGISTER} : Register")
    #other options here
    print(f"\t{EXIT} : Exit")

def handle_user_option():
    option = LOGIN
    while option != EXIT:
        print_main_menu()
        option = int(input("\n\tCommand: "))
        if option == REGISTER:
            user_service.register()
        elif option == EXIT:
            clear_console()
            return
        #other option here
        if user_service.current_user != None:
            clear_console()
            handle_account_option()
        
        clear_console()