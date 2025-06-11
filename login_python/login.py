import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import requests
import random
import string
import super_admin  # Import the super admin module
import admin_dashboard

API_URL = "http://127.0.0.1:5000"

def generate_captcha_text():
    characters = string.ascii_letters + string.digits + "!@#$%&"
    return ''.join(random.choices(characters, k=6))

def generate_captcha_image(text):
    image = Image.new('RGB', (180, 50), color=(240, 240, 240))
    draw = ImageDraw.Draw(image)
    
    for _ in range(200):
        x = random.randint(0, 180)
        y = random.randint(0, 50)
        draw.point((x, y), fill=(random.randint(200, 255), random.randint(200, 255), random.randint(200, 255)))
    
    for _ in range(3):
        start = (random.randint(0, 50), random.randint(0, 50))
        end = (random.randint(130, 180), random.randint(0, 50))
        draw.line([start, end], fill=(200, 200, 200), width=1)
    
    font = ImageFont.truetype("arial.ttf", 24)
    draw.text((20, 10), text, font=font, fill=(50, 50, 50))
    
    return ImageTk.PhotoImage(image)

def show_login_page(role):
    role_selection_window.destroy()  
    global login_window, username_entry, password_entry, sec_ans1_entry, sec_ans2_entry, captcha_text, captcha_entry, captcha_label

    login_window = tk.Tk()
    login_window.title(f"{role} Login")
    login_window.geometry("600x550")
    login_window.configure(bg='#f0f2f5')

    login_frame = tk.Frame(login_window, bg='white', borderwidth=1, relief='solid')
    login_frame.place(relx=0.5, rely=0.5, anchor='center', width=480, height=500)

    header_label = tk.Label(login_frame, text=f"{role} Login", 
                             font=("Arial", 16, "bold"),
                             fg='#1877f2', 
                             bg='white')
    header_label.pack(pady=(20, 15))

    username_frame = tk.Frame(login_frame, bg='white')
    username_frame.pack(fill='x', padx=40, pady=5)
    tk.Label(username_frame, text="Username", 
             font=("Arial", 10),
             bg='white', 
             fg='#606770').pack(anchor='w')
    username_entry = tk.Entry(username_frame, 
                               font=("Arial", 11),
                               width=30, 
                               bd=1, 
                               relief='solid')
    username_entry.pack(fill='x')

    password_frame = tk.Frame(login_frame, bg='white')
    password_frame.pack(fill='x', padx=40, pady=5)
    tk.Label(password_frame, text="Password", 
             font=("Arial", 10),
             bg='white', 
             fg='#606770').pack(anchor='w')
    password_entry = tk.Entry(password_frame, 
                               show="*", 
                               font=("Arial", 11),  
                               width=30, 
                               bd=1, 
                               relief='solid')
    password_entry.pack(fill='x')

    sec_ans1_entry = None
    sec_ans2_entry = None
    if role in ["Voter", "Admin", "EC (Super Admin)"]:
        security_frame = tk.Frame(login_frame, bg='white')
        security_frame.pack(fill='x', padx=40, pady=5)  
        
        tk.Label(security_frame, text="Security Question 1: What is your birth city?", 
                 font=("Arial", 10),  
                 bg='white', 
                 fg='#606770').pack(anchor='w')
        sec_ans1_entry = tk.Entry(security_frame, 
                              font=("Arial", 11), 
                              width=30, 
                              bd=1, 
                              relief='solid')
        sec_ans1_entry.pack(fill='x', pady=(0, 5))
        
        tk.Label(security_frame, text="Security Question 2: What is your favorite color?", 
                 font=("Arial", 10),
                 bg='white', 
                 fg='#606770').pack(anchor='w')
        sec_ans2_entry = tk.Entry(security_frame, 
                              font=("Arial", 11),
                              width=30, 
                              bd=1, 
                              relief='solid')
        sec_ans2_entry.pack(fill='x')

    captcha_frame = tk.Frame(login_frame, bg='white')
    captcha_frame.pack(fill='x', padx=40, pady=5)  
    
    captcha_text = generate_captcha_text()
    captcha_label = tk.Label(captcha_frame, bg='white')
    captcha_label.pack(side='left', padx=(0, 10))

    def update_captcha():
        global captcha_text  
        captcha_text = generate_captcha_text()
        captcha_image = generate_captcha_image(captcha_text)
        captcha_label.config(image=captcha_image)
        captcha_label.image = captcha_image

    update_captcha()  

    refresh_button = tk.Button(captcha_frame, 
                                text="🔄", 
                                command=update_captcha, 
                                font=("Arial", 16),  
                                bg='#f0f2f5', 
                                relief='flat')
    refresh_button.pack(side='left')

    captcha_entry_frame = tk.Frame(login_frame, bg='white')
    captcha_entry_frame.pack(fill='x', padx=40, pady=5)  
    tk.Label(captcha_entry_frame, text="Enter CAPTCHA", 
             font=("Arial", 10),  
             bg='white', 
             fg='#606770').pack(anchor='w')
    captcha_entry = tk.Entry(captcha_entry_frame, 
                              font=("Arial", 11),  
                              width=30, 
                              bd=1, 
                              relief='solid')
    captcha_entry.pack(fill='x')

    button_frame = tk.Frame(login_frame, bg='white')
    button_frame.pack(fill='x', padx=40, pady=10)

    back_button = tk.Button(button_frame, 
                             text="Back", 
                             command=lambda: go_back_to_roles(login_window), 
                             bg='#ff4d4d', 
                             fg='white', 
                             font=("Arial", 11, "bold"),
                             width=15, 
                             relief='flat')
    back_button.pack(side='left', padx=5)

    def login_with_captcha():
        username = username_entry.get()
        password = password_entry.get()
        entered_captcha = captcha_entry.get().strip()
        
        if role in ["Voter", "Admin", "EC (Super Admin)"]:
            if sec_ans1_entry is None or sec_ans2_entry is None:
                messagebox.showerror("Error", "Security entries not initialized!")
                return

            security_ans1 = sec_ans1_entry.get().lower().strip()
            security_ans2 = sec_ans2_entry.get().lower().strip()
            
            if not username or not password or not security_ans1 or not security_ans2 or entered_captcha != captcha_text:
                messagebox.showerror("Error", "Invalid credentials or CAPTCHA!")
                return
            
            response = requests.post(f"{API_URL}/login", json={
                "username": username, 
                "password": password, 
                "security_ans1": security_ans1, 
                "security_ans2": security_ans2,
                "role": role
            })
        else:
            if not username or not password or entered_captcha != captcha_text:
                messagebox.showerror("Error", "Invalid credentials or CAPTCHA!")
                return
            
            response = requests.post(f"{API_URL}/login", json={
                "username": username, 
                "password": password, 
                "role": role
            })
        
        data = response.json()
        
        print("DEBUG: API Response ->", data)  
        if data["success"]:
            messagebox.showinfo("Success", data["message"])
            login_window.destroy()
            if data["role"] == "Voter":
                open_face(username)
                open_voting_portal(username)
            elif data["role"] == "Admin": 
                open_admin_dashboard()
            elif data["role"] == "EC (Super Admin)":
                # Launch Super Admin Page
                super_admin.ECAdminPage.main()
        else:
            messagebox.showerror("Error", data["message"])

    login_button = tk.Button(button_frame, 
                              text="Login", 
                              command=login_with_captcha, 
                              bg='#1877f2', 
                              fg='white', 
                              font=("Arial", 11, "bold"),
                              width=15, 
                              relief='flat')
    login_button.pack(side='left', padx=5)

    login_window.mainloop()

def go_back_to_roles(window):
    window.destroy()
    show_role_selection()



def open_face(username):
    import face.face
    face.face.update_frame(username)

def open_admin_dashboard():
    import admin_dashboard 
    admin_dashboard.launch_admin_dashboard()

def open_news_portal():
    import news
    news.launch_news_portal()

def show_role_selection():
    global role_selection_window
    role_selection_window = tk.Tk()
    role_selection_window.title("E-Voting Portal")
    role_selection_window.geometry("600x500")
    role_selection_window.configure(bg='#f0f2f5')

    main_frame = tk.Frame(role_selection_window, bg='white', borderwidth=1, relief='solid')
    main_frame.place(relx=0.5, rely=0.5, anchor='center', width=480, height=400)

    header_label = tk.Label(main_frame, 
                            text="Election Commission of India\nE-Voting Portal", 
                            font=("Arial", 20, "bold"), 
                            fg='#1877f2', 
                            bg='white', 
                            justify='center')
    header_label.pack(pady=(40, 30))

    tk.Label(main_frame, 
             text="Select Your Login Role", 
             font=("Arial", 14), 
             fg='#606770', 
             bg='white').pack(pady=(0, 20))

    button_frame = tk.Frame(main_frame, bg='white')
    button_frame.pack(pady=10)

    roles = [
        ("Voter", "#6495ED"),
        ("Admin", "#228B22"),
        ("EC (Super Admin)", "#FFA500")
    ]

    for role, color in roles:
        btn = tk.Button(button_frame, 
                        text=role, 
                        command=lambda r=role: show_login_page(r), 
                        bg=color, 
                        fg='white', 
                        font=("Arial", 12, "bold"), 
                        width=20, 
                        relief='flat')
        btn.pack(pady=6)

     
    news_button = tk.Button(button_frame,
                            text="Election News",
                            command=open_news_portal,
                            bg="#1a73e8",
                            fg='white',
                            font=("Arial", 12, "bold"),
                            width=20,
                            relief='flat')
    news_button.pack(pady=6)

 

    role_selection_window.mainloop()

show_role_selection()