import sqlite3
import pandas as pd

def init_db():
    # Creates a local database file on your computer/mobile cache
    conn = sqlite3.connect("worklog_data.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn

def save_entry(conn, text):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (raw_text) VALUES (?)", (text,))
    conn.commit()

def load_history(conn):
    return pd.read_sql_query("SELECT timestamp, raw_text FROM logs ORDER BY timestamp DESC", conn)
