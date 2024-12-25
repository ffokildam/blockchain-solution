import sqlite3
from passlib.context import CryptContext
from defi_api import DeFiAPI  # Assuming DeFiAPI class is available in this file

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DB_PATH = "sqlite.db"


def create_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create users table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            address TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()


# Hash the password
def hash_password(password: str):
    return pwd_context.hash(password)


# Verify the password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Register a new user
def register_user(username: str, password: str):
    # Initialize DeFiAPI instance
    api = DeFiAPI()

    # Check if the user already exists
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    existing_user = c.fetchone()
    if existing_user:
        conn.close()
        return False  # User already exists

    # Hash the password
    hashed_password = hash_password(password)

    # Call create_new_user method to generate address
    address = api.create_new_user(password)  # Using the password passed to create a new user

    # Insert the new user into the database
    c.execute('INSERT INTO users (username, password, address) VALUES (?, ?, ?)',
              (username, hashed_password, address))
    conn.commit()
    conn.close()

    return address


# Authenticate a user
def authenticate_user(username: str, password: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Get the user from the database
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()

    if user and verify_password(password, user[1]):  # user[1] is the hashed password
        # Unlock the user's Ethereum account using their address and password
        api = DeFiAPI()
        api.unlock_account(user[2], password)  # user[2] is the stored address

        conn.close()
        return user[2]  # Return address if authentication is successful
    else:
        conn.close()
        return None  # Authentication failed
