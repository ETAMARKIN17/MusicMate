import sqlite3
import hashlib

# Connect to SQLite database (create it if it doesn't exist)
def create_users_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                   user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT UNIQUE NOT NULL,
                   password TEXT NOT NULL
               )''')

    # Commit changes and close connection
    conn.commit()
    conn.close()


def hash_password(password):
    # Create a SHA-256 hash of the password
    return hashlib.sha256(password.encode()).hexdigest()


def register_user():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    while True:
        username = input("Enter a username: ")
        if username.isdigit():
            print("Username cannot be only numbers. Please choose a different username.")
        else:
            break    
    
    password = input("Enter a password: ")
    #hashed_password = hash_password(password)
    hashed_password = password

    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        user_id = c.lastrowid  # Get the ID of the newly created user
        print(f"Registration successful! Your user ID is {user_id}.")
    except sqlite3.IntegrityError:
        print("Username already exists. Please choose a different username.")

    conn.close()

def login_user():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    while True:
        username_or_id = input("Enter your username or user ID: ")
        password = input("Enter your password: ")
        #hashed_password = hash_password(password)
        hashed_password = password

        c.execute("SELECT * FROM users WHERE (username=? OR user_id=?) AND password=?", (username_or_id, username_or_id, hashed_password))
        user = c.fetchone()

        if user:
            print(f"Welcome back, {user[1]}!")
            conn.close()
            return user  # Return user info for further use
        else:
            print("Incorrect username or password. Please try again.")

def show_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users")
    users = c.fetchall()

    if users:
        #print("User ID | Username  | Hashed Password")
        print("User ID | Username  | Password")
        print("-------------------------------------")
        for user in users:
            print(f"{user[0]:7} | {user[1]:8} | {user[2]}")
    else:
        print("No users found in the database.")

    conn.close()


def clear_whole_db():
    check1 = input("ARE YOU SURE YOU WANT TO CLEAR THE WHOLE TABLE?? (Enter 'Yes' if yes): ")
    if check1 == 'Yes':
        check2 = input("ARE YOU SURE?? (Enter 'YES I AM SURE' if yes): ")
        if check2 == 'YES I AM SURE':
            check3 = input("LAST CHECK!!!! (Enter 'i aM 100% PosITiVe I waNT tO clEaR' if yes): ")
            if check3 == 'i aM 100% PosITiVe I waNT tO clEaR':
                print('CONFIRMATION SUCCESS: Clearing Now')
                conn = sqlite3.connect('users.db')
                c = conn.cursor()

                # Drop users table if it exists
                c.execute('DROP TABLE IF EXISTS users')

                # Commit changes and close connection
                conn.commit()
                conn.close()
            else:
                print("Did not type exactly not clearing")
        else:
            print("Did not type exactly not clearing")
    else:
        print("Did not type exactly not clearing")


# Call this function once to create the table if it doesn't exist
create_users_table()
