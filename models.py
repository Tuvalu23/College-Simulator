# models.py

import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = "users.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    # Create simulations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS simulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            university_name TEXT NOT NULL,
            result TEXT NOT NULL CHECK(result IN ('acceptance', 'rejection', 'deferred', 'waitlist', 'edacceptance', 'wacceptance', 'wrejection')),
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return generate_password_hash(password)

class User:
    @staticmethod
    def create(username, password):
        hashed_password = hash_password(password)
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
            conn.commit()

    @staticmethod
    def get_by_username(username):
        with sqlite3.connect(DATABASE) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row["id"],
                    "username": row["username"],
                    "password_hash": row["password_hash"]
                }
            return None
    
    @staticmethod
    def get_by_id(user_id):
        with sqlite3.connect(DATABASE) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row["id"],
                    "username": row["username"]
                }
            return None

    @staticmethod
    def verify_password(stored_hash, provided_password):
        return check_password_hash(stored_hash, provided_password)
    
    @staticmethod
    def delete_user(user_id):
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            
    @staticmethod
    def get_simulations(user_id):
        with sqlite3.connect(DATABASE) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT university_name, result, timestamp
                FROM simulations
                WHERE user_id = ?
            ''', (user_id,))
            rows = cursor.fetchall()
            simulations = []
            for row in rows:
                simulations.append({
                    'university_name': row['university_name'],
                    'result': row['result'],
                    'timestamp': row['timestamp']
                })
            return simulations

    @staticmethod
    def log_simulation(user_id, university_name, result):
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO simulations (user_id, university_name, result)
                VALUES (?, ?, ?)
            ''', (user_id, university_name, result))
            conn.commit()
