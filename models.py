import sqlite3
import hashlib

DATABASE = "users.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class User:
    @staticmethod
    def create(username, password):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_username(username):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {
                "id": row[0],
                "username": row[1],
                "password_hash": row[2]
            }
        return None

    @staticmethod
    def verify_password(stored_hash, password):
        return stored_hash == hash_password(password)
