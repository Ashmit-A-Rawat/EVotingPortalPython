import tkinter as tk
from tkinter import ttk
import requests
import webbrowser

API_KEY = "60cbf3de60f84d66a80660989436a280"
BASE_URL = "https://newsapi.org/v2/everything"

def fetch_election_news():
    query = "election"
    language = language_var.get()

    params = {
        'q': query,
        'language': language,
        'sortBy': 'publishedAt',
        'apiKey': API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    for widget in news_frame.winfo_children():
        widget.destroy()

    if data["status"] == "ok":
        articles = data["articles"]
        for i, article in enumerate(articles[:10], 1):
            title = article["title"]
            description = article["description"] or "No description"
            url = article["url"]

            # News Card
            card = tk.Frame(news_frame, bg="#ffffff", bd=1, relief="ridge")
            card.pack(fill="x", pady=10, padx=20)

            title_label = tk.Label(card, text=f"{i}. {title}",
                                   font=("Segoe UI", 12, "bold"),
                                   bg="#ffffff", fg="#000000", wraplength=700, justify="left")
            title_label.pack(anchor="w", padx=10, pady=(10, 2))

            desc_label = tk.Label(card, text=description,
                                  font=("Segoe UI", 10),
                                  bg="#ffffff", fg="#444444", wraplength=700, justify="left")
            desc_label.pack(anchor="w", padx=10, pady=(0, 5))

            link_label = tk.Label(card, text="🔗 Read more", cursor="hand2",
                                  font=("Segoe UI", 10, "underline"),
                                  bg="#ffffff", fg="#1a73e8")
            link_label.pack(anchor="w", padx=10, pady=(0, 10))
            link_label.bind("<Button-1>", lambda e, url=url: open_link(url))
    else:
        error_label = tk.Label(news_frame, text="❌ Failed to fetch election news.",
                               font=("Segoe UI", 12), bg="#f0f0f0", fg="red")
        error_label.pack()

def open_link(url):
    webbrowser.open(url)

app = tk.Tk()
app.title("🗳️ Election News Portal")
app.geometry("900x700")
app.configure(bg="#f0f0f0")

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#f0f0f0", foreground="#000000", font=("Segoe UI", 12))
style.configure("TButton",
                background="#1a73e8",
                foreground="white",
                font=("Segoe UI", 11, "bold"),
                padding=10)
style.map("TButton",
          background=[("active", "#155ab6")])

title_label = tk.Label(app,
                       text="🗳️ Real-Time Election News",
                       bg="#f0f0f0",
                       fg="#000000",
                       font=("Segoe UI", 22, "bold"),
                       pady=10)
title_label.pack()

top_frame = ttk.Frame(app)
top_frame.pack(pady=10)

language_var = tk.StringVar(value="en")
ttk.Label(top_frame, text="Language:").grid(row=0, column=0, padx=5)

language_menu = ttk.Combobox(top_frame, textvariable=language_var,
                             values=["en", "hi"],
                             font=("Segoe UI", 10),
                             width=10)
language_menu.grid(row=0, column=1, padx=5)

fetch_button = ttk.Button(app, text="🔍 Fetch News", command=fetch_election_news)
fetch_button.pack(pady=10)

canvas = tk.Canvas(app, bg="#f0f0f0", highlightthickness=0)
scrollbar = ttk.Scrollbar(app, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

news_frame = scrollable_frame

app.mainloop()
