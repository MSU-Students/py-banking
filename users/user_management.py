import random
from account import handle_account_option
from utils import clear_console
enter = False

class User:
    def __init__(self, User_Id='', pin='',address = '', bday='', fullname='', mob_num='', authentication= 0, email = '', nationality='', approval=0):
        self.User_Id = User_Id
        self.pin = pin
        self.name = fullname
        self.mobile_number = mob_num
        self.address = address
        self.bday = bday
        self.authentication = authentication
        self.email = email
        self.nationality = nationality
        self.approval = approval

class UserService:
    registered_user = User()
    login_user = User()

    def login(self):
        self.user_id = input("User ID:\t\t")
        self.pin = input("Password:\t\t")
        self.login_user = User(self.user_id, self.pin)
    
    def register(self):
        self.full_name = input("Full Name:\t\t")
        self.mobile_num = input("Mobile Number:\t\t")
        self.address = input("Address:\t\t")
        self.bday = input ("Birthdate:\t\t")
        self.email = input("Email Address:\t\t")
        self.nationality = input("Nationality:\t\t")
        self.user_id = input("User ID:\t\t")
        self.pin = input("Password:\t\t")
        self.approval = 0 #false
        self.authentication = str(random.randint(10000, 99999))

        with open(self.user_id + ".txt", 'a') as account:
            account.write(self.full_name + '\n')
            account.write(self.mobile_num + '\n')
            account.write(self.address + '\n')
            account.write(self.bday + '\n') 
            account.write(self.email + '\n')
            account.write(self.nationality + '\n')
            account.write(self.user_id + '\n')
            account.write(self.pin + '\n')
            account.write(str(self.approval) + '\n')
            account.write(self.authentication +'\n')
        self.registered_user = User(self.user_id, self.pin, self.address, self.bday ,self.full_name, self.mobile_num, self.authentication, self.email, self.nationality, self.approval)
        print ('You have succesfully registered an account')

    def forgot_password(self):
        print ("Enter the right following information for user authentication")
        self.proof_accnum = input('Enter User Account Number:\t\t')
        self.proof = input('Enter User Authentication:\t\t')

        try:
            with open (self.proof_accnum + ".txt", 'r') as account:
                lines = account.readlines()
                if len(lines) >= 7:
                    self.security_number = lines[6].strip()
        except FileNotFoundError as e:
            print("Error: Account Doesn't Exist")
            input('Press any key to continue')
        except NotADirectoryError as e:
            print("Error: Account Doesn't Exist")
            input('Press any key to continue')
        else: 
            if self.proof == self.security_number:
                print("you can now change your password")
                self.pin = input("New Password:\t")
                self.confirm_pin = input("confirm Password:\t")
                
                if self.pin == self.confirm_pin:
                    if len(lines) >= 7:
                        lines[5] = self.pin + '\n'
                    with open(self.proof_accnum + ".txt", 'w') as account:
                        account.writelines(lines)    
                    print("You have succesfully changed your password!")
                    return True

    #Todo Other methods such as (change_pin, update_profile)

User_service = UserService()


EXIT, LOGIN, REGISTER, FORGOT_PASS = (0, 1, 2, 3)
def print_main_menu():
    print("Options:")
    print(f"\t{LOGIN} : Login")
    print(f"\t{REGISTER} : Register")
    print(f"\t{FORGOT_PASS} : Forgot Password")
    print(f"\t{EXIT} : Exit")

def handle_user_option():
    key = False
    global enter
    option = LOGIN
    while option != EXIT:
        print_main_menu()
        option = int(input("\n\tCommand: "))

#register
        if option == REGISTER:
            print("Registration")
            User_service.register()

    
#login method
        elif option == LOGIN:
            print("Login")  
            User_service.login()
            try:
                with open (User_service.login_user.User_Id + ".txt", 'r') as account:
                    lines = account.readlines()
                    if len(lines) >= 9:
                        user_id = lines[6].strip()
                        password = lines[7].strip()
            except NotADirectoryError as e:
                print("Error: Account Doesn't Exist")
                input('Press any key to continue')
            except  FileNotFoundError as e:
                print("Error: Account Doesn't Exist")
                input('Press any key to continue')
            else:
                if User_service.login_user.User_Id != user_id and User_service.login_user.pin != password:
                    print("Invalid username or pin")
                    input('wrong')
                    clear_console()
                    continue

                with open(User_service.login_user.User_Id + '.txt', 'r') as account:
                    lines = account.readlines()
                    if len(lines) >= 9:
                        key = int(lines[8])
                        if key == 0: print("Account hasn't been confirmed by the Admin")
                        input("press enter to continue")

        elif option == FORGOT_PASS:
            if User_service.forgot_password():
                User_service.login()

        elif option == EXIT:
            clear_console()
            return
           
        if key:
            clear_console()
            print(f"Welcome {User_service.registered_user.name}")
            handle_account_option() #pagador, alfred, kurt, and eiman
        
        clear_console()