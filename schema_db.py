import sqlite3

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect('mental_health.db')

# Create a cursor object to execute SQL commands
cur = conn.cursor()

# Create the users table if it doesn't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        gender TEXT NOT NULL CHECK (gender IN ('Male', 'Female', 'Nonbinary')),
        dob DATE NOT NULL,
        username TEXT NOT NULL,
        hash TEXT NOT NULL
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            user_id INTEGER NOT NULL,
            date DATE NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id))
''')



# Save (commit) the changes and close the connection
conn.commit()
conn.close()
