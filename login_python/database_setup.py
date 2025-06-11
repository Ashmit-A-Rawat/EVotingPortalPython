import sqlite3
from bcrypt import hashpw, gensalt

def setup_database():
    conn = sqlite3.connect("evoting.db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS voters (
                        username TEXT PRIMARY KEY,
                        has_voted TEXT DEFAULT 'No')''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS votes2 (
                        party_name TEXT PRIMARY KEY,
                        vote_count INTEGER DEFAULT 0)''')

  
    cursor.execute('''CREATE TABLE IF NOT EXISTS election_status (
                        id INTEGER PRIMARY KEY CHECK (id = 1), 
                        is_active INTEGER DEFAULT 1)''')

    
    cursor.execute("INSERT OR IGNORE INTO election_status (id, is_active) VALUES (1, 1)")

    parties = [("Bhartiya Janta Party", 0), ("Aam Aadmi Party", 0), ("Congress", 0), ("Communist Party of India", 0), ("Samajwadi Party", 0)]
    cursor.executemany("INSERT OR IGNORE INTO votes2 (party_name, vote_count) VALUES (?, ?)", parties)


    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        password TEXT NOT NULL,
                        security_ans1 TEXT NOT NULL,
                        security_ans2 TEXT NOT NULL,
                        role TEXT NOT NULL,
                        voted INTEGER DEFAULT 0)''')


    users = [
        ("ashmit", hashpw("ashmit1".encode(), gensalt()).decode(), "mumbai", "blue", "Voter"),
        ("dhruv", hashpw("dhruv2".encode(), gensalt()).decode(), "delhi", "red", "Voter"),
        ("pratik", hashpw("pratik3".encode(), gensalt()).decode(), "pune", "green", "Voter"),
        ("hardik", hashpw("hardik4".encode(), gensalt()).decode(), "chennai", "yellow", "Voter"),
        ("dhruv1", hashpw("adminpass1".encode(), gensalt()).decode(), "mumbai", "orange", "Admin"),
        ("hardik2", hashpw("adminpass2".encode(), gensalt()).decode(), "banglore", "white", "Admin"),
        ("ashmit3", hashpw("adminpass3".encode(), gensalt()).decode(), "nagpur", "black", "Admin"),
        ("superadmin", hashpw("superpass".encode(), gensalt()).decode(), "mumbai", "orange", "SuperAdmin"),
    ]

    cursor.executemany("INSERT OR IGNORE INTO users (username, password, security_ans1, security_ans2, role) VALUES (?, ?, ?, ?, ?)", users)

    cursor.execute('''INSERT OR IGNORE INTO voters (username) 
                  SELECT username FROM users WHERE role = 'Voter' ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
