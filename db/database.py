import sqlite3
import os

DATA_FOLDER = "Data"
DATA_PATH = os.path.join(DATA_FOLDER, "documents.db")

# creates a connection to the SQLite database, creating the file if it doesn't exist
def create_connection():
    os.makedirs(DATA_FOLDER, exist_ok=True)
    conn = sqlite3.connect(DATA_PATH)
    return conn

# Initialize the database and create tables if they don't exist
def init_db():
    conn=create_connection()
    cursor=conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   path TEXT,
                   thumbnail_path TEXT,
                   tags TEXT,
                   description TEXT,
                   upload_date TEXT,
                   lecturer_date TEXT,
                   total_pages INTEGER
                   )
                   ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS page_visits (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   document_id INTEGER,
                   page_number INTEGER,
                   timestamp TEXT
                   )
                   ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS App_Visit (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   event_type TEXT,
                   timestamp TEXT
                   )
    ''')
    conn.commit()
    conn.close()