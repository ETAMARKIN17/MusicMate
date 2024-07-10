from user_accounts import *  # Import user account functions


def intro_page():
    """
    Displays the home screen with options to login, register, or exit.

    Returns:
    - str: Choice made by the user ('login', 'register', 'exit').
    """
    while True:
        print("\nWelcome to WeatherTunes! 🌤️ 🎶")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            return 'login'
        elif choice == '2':
            return 'register'
        elif choice == '3':
            return 'exit'
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
