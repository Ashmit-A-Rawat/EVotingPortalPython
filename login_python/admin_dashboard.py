import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

def connect_db():
    return sqlite3.connect("evoting.db")

def update_live_voting_counts(voter_count_label, votes_labels):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(vote_count) FROM votes2")
    total_votes_cast = cursor.fetchone()[0] or 0 

    cursor.execute("SELECT COUNT(*) FROM voters")
    total_voters = cursor.fetchone()[0]

    cursor.execute("SELECT party_name, vote_count FROM votes2")
    votes_data = dict(cursor.fetchall())  
    conn.close()

    voter_count_label.config(text=f"Total Votes Cast: {total_votes_cast}")

    parties = ["Bhartiya Janta Party", "Aam Aadmi Party", "Congress", "Communist Party of India", "Samajwadi Party"]
    emojis = ["🌙", "🔥", "⭐", "🚀", "🌿"]

    for i in range(5):
        vote_count = votes_data.get(parties[i], 0)
        votes_labels[i].config(text=f"{parties[i]} Votes ({emojis[i]}): {vote_count}")

def terminate_election(voter_count_label, votes_labels):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM votes2")
    
    cursor.execute("UPDATE voters SET has_voted = 'No'")
    
    parties = ["Bhartiya Janta Party", "Aam Aadmi Party", "Congress", "Communist Party of India", "Samajwadi Party"]
    for party in parties:
        cursor.execute("INSERT INTO votes2 (party_name, vote_count) VALUES (?, ?)", (party, 0))

    conn.commit()
    conn.close()

    update_live_voting_counts(voter_count_label, votes_labels)
    messagebox.showinfo("Election Terminated", "Election terminated. All votes reset.")

# Function to hold election
def hold_election():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE election_status SET is_active = 0 WHERE id = 1")
    conn.commit()
    conn.close()

    messagebox.showinfo("Election Held", "Election is now on hold.")

# Function to resume election
def resume_election():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE election_status SET is_active = 1 WHERE id = 1")
    conn.commit()
    conn.close()

    messagebox.showinfo("Election Resumed", "Election has been resumed.")

# Function to show voters
def show_voters():
    voter_window = tk.Toplevel()
    voter_window.title("Voters List")
    voter_window.geometry("400x400")

    search_frame = tk.Frame(voter_window)
    search_frame.pack(pady=10)

    search_entry = tk.Entry(search_frame, width=20)
    search_entry.pack(side=tk.LEFT, padx=5)

    search_button = tk.Button(search_frame, text="Search", command=lambda: fetch_voters(search_entry.get(), voter_tree))
    search_button.pack(side=tk.LEFT)

    columns = ("Username", "Has Voted")
    voter_tree = ttk.Treeview(voter_window, columns=columns, show="headings")
    
    voter_tree.heading("Username", text="Voter Username")
    voter_tree.heading("Has Voted", text="Has Voted")
    
    voter_tree.pack(fill="both", expand=True)
    
    fetch_voters("", voter_tree)

# Function to fetch and display voters
def fetch_voters(search_text, tree):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT username, has_voted FROM voters WHERE username LIKE ?", ('%' + search_text + '%',))
    rows = cursor.fetchall()
    conn.close()

    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", "end", values=row)

# Function to download voters list
def download_voters_list():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT username, has_voted FROM voters")
    rows = cursor.fetchall()
    conn.close()

    with open("voters_list.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Voter Username", "Has Voted"])
        writer.writerows(rows)

    messagebox.showinfo("Download Successful", "Voters list downloaded as 'voters_list.csv'")

def logout(admin_root):
    admin_root.destroy()
    os.system("python login.py") 

def launch_admin_dashboard():
    admin_root = tk.Tk()
    admin_root.title("Admin Dashboard")
    admin_root.geometry("600x400")
    admin_root.configure(bg="#D3D3D3")

    frame = tk.Frame(admin_root, bg="#D3D3D3")
    frame.pack(pady=20)

    terminate_button = tk.Button(frame, text="Terminate Election", bg="red", fg="white", width=20, 
                                 command=lambda: terminate_election(voter_count_label, votes_labels))
    hold_button = tk.Button(frame, text="Hold Election", bg="orange", fg="black", width=20, command=hold_election)
    resume_button = tk.Button(frame, text="Resume Election", bg="green", fg="white", width=20, command=resume_election)
    show_voters_button = tk.Button(frame, text="Show Voters", width=20, command=show_voters)
    download_button = tk.Button(frame, text="Download Voters List", width=20, command=download_voters_list)
    logout_button = tk.Button(frame, text="Logout", bg="red", fg="white", width=20, command=lambda: logout(admin_root))

    terminate_button.grid(row=0, column=0, padx=10, pady=5)
    hold_button.grid(row=0, column=1, padx=10, pady=5)
    resume_button.grid(row=1, column=0, padx=10, pady=5)
    show_voters_button.grid(row=1, column=1, padx=10, pady=5)
    download_button.grid(row=2, column=0, padx=10, pady=5)
    logout_button.grid(row=2, column=1, padx=10, pady=5)

    # Vote count labels
    voter_count_label = tk.Label(admin_root, text="Total Votes Cast: 0", font=("Arial", 14), bg="#D3D3D3")
    votes_labels = [
        tk.Label(admin_root, text="Bhartiya Janta Party Votes (🌙): 0", bg="#D3D3D3"),
        tk.Label(admin_root, text="Aam Aadmi Party Votes (🔥): 0", bg="#D3D3D3"),
        tk.Label(admin_root, text="Congress Votes (⭐): 0", bg="#D3D3D3"),
        tk.Label(admin_root, text="Communist Party of India Votes (🚀): 0", bg="#D3D3D3"),
        tk.Label(admin_root, text="Samajwadi Party Votes (🌿): 0", bg="#D3D3D3"),
    ]

    voter_count_label.pack()
    for label in votes_labels:
        label.pack()

    update_live_voting_counts(voter_count_label, votes_labels)
    
    def refresh_counts():
        update_live_voting_counts(voter_count_label, votes_labels)
        admin_root.after(5000, refresh_counts) 
    
    admin_root.after(5000, refresh_counts)
    
    admin_root.mainloop()

if __name__ == "__main__":
    launch_admin_dashboard()