import sqlite3

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect('mental_health.db')

# Create a cursor object to execute SQL commands
cur = conn.cursor()

# Create the users table if it doesn't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

# Save (commit) the changes and close the connection
conn.commit()
conn.close()
