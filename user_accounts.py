import sqlite3
import hashlib
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


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
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  (username, hashed_password))
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
    c.execute("SELECT * FROM users WHERE (username=? OR user_id=?) AND password=?",
              (username_or_id, username_or_id, hashed_password))
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


# Call this function once to create the table if it doesn't exist
create_users_table()
