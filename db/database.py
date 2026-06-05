import sqlite3
import os

DATA_PATH=os.path.join("Data","documents.db")

def create_connection():
    conn = sqlite3.connect(DATA_PATH)
    return conn

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