import os

def main():
    print("Welcome to PY Banking")
    if not os.path.exists('data/'):
        os.mkdir('data')
    from users import handle_user_option
    handle_user_option()

if __name__ == '__main__':
    main()