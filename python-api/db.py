import sqlite3
from passlib.context import CryptContext
from defi_api import DeFiAPI  # Assuming DeFiAPI class is available in this file

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DB_PATH = "sqlite.db"


def create_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            address TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def register_user(username: str, password: str):
    api = DeFiAPI()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    existing_user = c.fetchone()
    if existing_user:
        conn.close()
        return False

    hashed_password = hash_password(password)

    address = api.create_new_user(password)

    c.execute('INSERT INTO users (username, password, address) VALUES (?, ?, ?)',
              (username, hashed_password, address))
    conn.commit()
    conn.close()

    return address


def authenticate_user(username: str, password: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()

    if user and verify_password(password, user[1]):
        api = DeFiAPI()
        api.unlock_account(user[2], password)

        conn.close()
        return user[2]
    else:
        conn.close()
        return None
