import sqlite3

def reset_votes():
    conn = sqlite3.connect("evoting.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET voted = 0") 
    cursor.execute("UPDATE voters SET has_voted = 'No'")  
    cursor.execute("UPDATE votes2 SET vote_count = 0")  
    conn.commit()
    conn.close()

    print("Vote statuses have been reset successfully.")

if __name__ == "__main__":
    reset_votes()
