import sqlite3

DATABASE = "app/database/personnel_tracking.db"

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn