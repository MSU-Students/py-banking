import os

def main():
    if not os.path.exists('data/'):
        os.mkdir('data')
    from users import handle_user_option
    handle_user_option()

if __name__ == '__main__':
    main()