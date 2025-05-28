import sqlite3

conn = sqlite3.connect('mental_health.db')
cur = conn.cursor

# Create user login table
cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL)
            ''')

conn.commit()
conn.close()