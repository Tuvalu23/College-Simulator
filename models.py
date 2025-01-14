import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import json

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
            result TEXT NOT NULL CHECK(
                result IN (
                    'acceptance','rejection','deferred','waitlist',
                    'edacceptance','wacceptance','wrejection',
                    'D/A','D/R','D/W','W/A','W/R','D/W/A','D/W/R'
                )
            ),
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            sim_type TEXT NOT NULL DEFAULT 'quick' CHECK(
                sim_type IN ('quick','advanced')
            ),
            adv_data TEXT,  -- JSON storing advanced-sim details
            app_type TEXT DEFAULT '',  -- Stores application type (optional)
            enrolled INTEGER NOT NULL DEFAULT 0,  -- 1 if user eventually enrolled
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
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                           (username, hashed_password))
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
        """Fetch *all* simulations for a given user (both quick and advanced)."""
        with sqlite3.connect(DATABASE) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT university_name, result, timestamp, sim_type, adv_data, enrolled
                FROM simulations
                WHERE user_id = ?
            ''', (user_id,))
            rows = cursor.fetchall()
            simulations = []
            for row in rows:
                simulations.append({
                    'university_name': row['university_name'],
                    'result': row['result'],
                    'timestamp': row['timestamp'],
                    'sim_type': row['sim_type'],
                    'adv_data': row['adv_data'],
                    'enrolled': row['enrolled']
                })
            return simulations
        
    def log_simulation(user_id, university_name, result, sim_type="quick", adv_data=None, enrolled=0, app_type='RD'):
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()

            # JSON-encode adv_data (if any)
            if adv_data is not None:
                adv_json = json.dumps(adv_data)
            else:
                adv_json = None

            # 1) Check if an identical simulation was already logged
            #    Adjust the WHERE clause to be as strict or loose as you want.
            #    This example checks if the user has already logged the EXACT same
            #    sim_type, result, and app_type *on the same day*.
            #    If you want an even stricter check, remove the date filters. 
            cursor.execute("""
            SELECT id
            FROM simulations
            WHERE user_id = ?
              AND university_name = ?
              AND result = ?
              AND sim_type = ?
              AND app_type = ?
              AND DATE(timestamp) = DATE('now')
            """, (user_id, university_name, result, sim_type, app_type))

            existing = cursor.fetchone()
            if existing:
                print("[DEBUG] log_simulation: Duplicate found, skipping insert.")
                return  # Skip insertion, so we don't add a new row.

            # 2) If we pass the above check, we insert
            print("[DEBUG] log_simulation: Creating new simulation record.")
            cursor.execute("""
            INSERT INTO simulations
                (user_id, university_name, result, sim_type, adv_data, enrolled, app_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, university_name, result, sim_type, adv_json, enrolled, app_type))

            conn.commit()

    @staticmethod
    def update_enrolled(user_id, university_name):
        """
        If the user chooses to enroll at a given university_name,
        mark the relevant advanced-sim row(s) as enrolled=1 for that user & college.
        For simplicity, you can do it for the user's last acceptance in that college.
        """
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            # We'll update all advanced sims for that user & college that had an acceptance-type result
            cursor.execute('''
                UPDATE simulations
                SET enrolled=1
                WHERE user_id=? AND university_name=? 
                      AND sim_type='advanced'
                      AND result IN (
                           'acceptance','edacceptance','wacceptance',
                           'D/A','W/A','D/W/A'
                      )
            ''', (user_id, university_name))
            conn.commit()
    
    @staticmethod
    def get_all_advanced_sims_for_college(college_short_name):
        """
        Return all advanced-sim rows for a given college (case-insensitive),
        across *all* users.
        """
        with sqlite3.connect(DATABASE) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM simulations
                WHERE lower(university_name) = lower(?)
                  AND sim_type = 'advanced'
            ''', (college_short_name,))
            rows = cursor.fetchall()
            results = []
            for row in rows:
                results.append({
                    'id': row['id'],
                    'user_id': row['user_id'],
                    'university_name': row['university_name'],
                    'result': row['result'],
                    'timestamp': row['timestamp'],
                    'sim_type': row['sim_type'],
                    'adv_data': row['adv_data'],
                    'enrolled': row['enrolled'],
                    'app_type': row['app_type']
                })
            return results
