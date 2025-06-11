import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3

class ECAdminPage:
    is_election_terminated = False

    @classmethod
    def main(cls):
        frame = tk.Tk()
        frame.title("EC Admin Page")
        frame.geometry("400x300")
        frame.configure(background='lightgray')

        frame.update_idletasks()
        width = frame.winfo_width()
        height = frame.winfo_height()
        x = (frame.winfo_screenwidth() // 2) - (width // 2)
        y = (frame.winfo_screenheight() // 2) - (height // 2)
        frame.geometry(f'400x300+{x}+{y}')

        declare_result_button = tk.Button(
            frame, 
            text="Declare Result", 
            width=20, 
            height=2
        )
        logout_button = tk.Button(
            frame, 
            text="Logout", 
            width=20, 
            height=2
        )

        declare_result_button.grid(
            row=0, 
            column=0, 
            padx=10, 
            pady=10
        )

        logout_button.grid(
            row=1, 
            column=0, 
            padx=10, 
            pady=10
        )

        # Attach action listeners
        declare_result_button.config(
            command=lambda: cls.declare_result(frame)
        )
        logout_button.config(
            command=lambda: cls.logout(frame)
        )

        # Start the main loop
        frame.mainloop()

    @classmethod
    def declare_result(cls, frame):
        if not cls.is_election_terminated:
            cls.update_live_voting_counts()
            cls.create_result_visualization()
        else:
            messagebox.showinfo(
                "Election Status", 
                "Election is terminated. No results available."
            )

    @classmethod
    def update_live_voting_counts(cls):
        """Update and print live voting counts"""
        print("Live voting counts updated.")

    @classmethod
    def create_result_visualization(cls):
        """
        Create result visualization with bar chart and pie chart
        Using actual data from the database
        """
        # Connect to the database
        conn = sqlite3.connect("evoting.db")
        cursor = conn.cursor()

        # Fetch party votes
        cursor.execute("SELECT party_name, vote_count FROM votes2")
        party_results = cursor.fetchall()

        # Separate parties and votes
        parties = [result[0] for result in party_results]
        party_votes = [result[1] for result in party_results]

        # Count total voters and voted voters
        cursor.execute("SELECT COUNT(*) FROM voters")
        total_voters = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM voters WHERE has_voted = 'Yes'")
        voted_voters = cursor.fetchone()[0]

        # Close database connection
        conn.close()

        # Create result window
        result_window = tk.Toplevel()
        result_window.title("Election Results")
        result_window.geometry("800x600")

        # Create matplotlib figure with subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
        fig.suptitle('Election Results Visualization')

        # Party Bar Chart
        ax1.bar(parties, party_votes, color=['blue', 'green', 'red', 'purple', 'orange'])
        ax1.set_title('Party-wise Votes')
        ax1.set_xlabel('Parties')
        ax1.set_ylabel('Number of Votes')
        
        # Add vote count labels on top of each bar
        for i, v in enumerate(party_votes):
            ax1.text(i, v, str(v), ha='center', va='bottom')

        turnout_data = [voted_voters, total_voters - voted_voters]
        turnout_labels = ['Voted', 'Not Voted']
        myexplode = [0.2, 0]
        ax2.pie(turnout_data, labels=turnout_labels, autopct='%1.1f%%',explode = myexplode,shadow = True, 
                colors=['green', 'red'])
        ax2.set_title('Voter Turnout')

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=result_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

    @classmethod
    def logout(cls, frame):
        print("Logging out")
        frame.destroy()

if __name__ == "__main__":
    ECAdminPage.main()