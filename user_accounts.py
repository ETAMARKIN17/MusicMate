import sqlite3
import hashlib
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Admin credentials
ADMIN_USERNAME = 'Admin'
ADMIN_PASSWORD = 'MainAdmin'

# Function to connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # Allows fetching rows as dictionaries
    return conn

# Create users table if not exists
def create_users_table():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                   user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT UNIQUE NOT NULL,
                   password TEXT NOT NULL
               )''')
    conn.commit()
    conn.close()

# Function to hash a password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to register a new user
def register_user(username, password):
    if username.isdigit():
        return None, "Username cannot be empty. Please choose a valid username."
    if len(username) < 5:
        return None, "Username must be longer than 5 characters. Please choose a valid username."
    
    conn = get_db_connection()
    c = conn.cursor()
    hashed_password = hash_password(password)
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        user_id = c.lastrowid
        conn.close()
        return user_id, None  # Return user ID and no error message if successful
    except sqlite3.IntegrityError:
        conn.close()
        return None, "Username already exists. Please choose a different username."

# Function to authenticate a user
def login_user(username_or_id, password):
    conn = get_db_connection()
    c = conn.cursor()
    hashed_password = hash_password(password)
    c.execute("SELECT * FROM users WHERE (username=? OR user_id=?) AND password=?", (username_or_id, username_or_id, hashed_password))
    user = c.fetchone()
    conn.close()
    return user

# Function to fetch a user by user ID
def get_user_by_id(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user

# Function to fetch all users (for testing or admin purposes)
def get_all_users():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return users

# Function to clear the entire users table (for development purposes)
def clear_users_table():
    check_confirmation = input("ARE YOU SURE YOU WANT TO CLEAR THE WHOLE TABLE? (Enter 'yes' to confirm): ").lower()
    if check_confirmation == 'yes':
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS users')
        conn.commit()
        conn.close()
        print('Users table cleared successfully.')
    else:
        print('Operation aborted.')

# Function to check if user is admin
def is_admin(user_id):
    user = get_user_by_id(user_id)
    if user and user['username'] == ADMIN_USERNAME and user['password'] == hash_password(ADMIN_PASSWORD):
        return True
    return False

# Call this function once to create the table if it doesn't exist
create_users_table()
