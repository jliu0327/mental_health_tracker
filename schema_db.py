import sqlite3

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect('mental_health.db')

# Create a cursor object to execute SQL commands
cur = conn.cursor()

# Create the users table if it doesn't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        gender TEXT NOT NULL CHECK (gender IN ('Male', 'Female', 'Nonbinary')),
        dob DATE NOT NULL,
        username TEXT NOT NULL,
        hash TEXT NOT NULL
    )
''')

# Create the entries table
cur.execute('''
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        date DATE NOT NULL,
        content TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

# Create the tracker table
cur.execute('''
    CREATE TABLE IF NOT EXISTS tracker (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        date DATE NOT NULL,
        mood TEXT NOT NULL,
        sleep TEXT NOT NULL,
        diet TEXT NOT NULL,
        energy TEXT NOT NULL,
        stress TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

# Create the goals table
cur.execute('''
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        goal_title TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        due_date DATE,
        priority TEXT CHECK (priority IN ('Low', 'Medium', 'High')) DEFAULT 'Medium',
        completed BOOLEAN DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

# Create the user_profile table
cur.execute('''
    CREATE TABLE IF NOT EXISTS user_profiles (
        user_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        middle_name TEXT,
        last_name TEXT NOT NULL,
        gender TEXT NOT NULL CHECK (gender IN ('Male', 'Female', 'Nonbinary')),
        birthday DATE,
        location TEXT,
        username TEXT NOT NULL,
        bio TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')


# Save (commit) the changes and close the connection
conn.commit()
conn.close()
