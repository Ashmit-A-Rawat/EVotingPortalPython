import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import face_recognition
import os
import sys
import numpy as np

# Initialize the Tkinter window
root = tk.Tk()
root.title("E-Voting Portal - Face Recognition Authentication")
root.geometry("800x600")
root.config(bg="#f5f5f5")

# Create a text widget for logging
log_frame = tk.Frame(root, bg="#f5f5f5")
log_frame.pack(side=tk.BOTTOM, fill=tk.X)

log_label = tk.Label(log_frame, text="Debug Log:", font=("Helvetica", 10, "bold"), bg="#f5f5f5", anchor="w")
log_label.pack(side=tk.TOP, anchor="w", padx=10)

log_text = tk.Text(log_frame, height=5, width=80, font=("Courier", 9))
log_text.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

def log_message(message):
    """Add message to log widget"""
    log_text.insert(tk.END, f"[DEBUG] {message}\n")
    log_text.see(tk.END)  # Auto-scroll to the end

# OpenCV video capture (Webcam)
try:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        log_message("Error: Could not open webcam. Check your camera connection.")
        messagebox.showerror("Error", "Could not open webcam.")
except Exception as e:
    log_message(f"Webcam initialization error: {str(e)}")
    messagebox.showerror("Error", f"Webcam initialization error: {str(e)}")

# Status variable
status_text = tk.StringVar()
status_text.set("Status: Waiting for face detection...")

# Load known faces from the database
def load_known_faces(database_dir="database"):
    known_faces = {}
    if not os.path.exists(database_dir):
        os.makedirs(database_dir)
        log_message(f"Created database directory: {database_dir}")
        return known_faces
    
    log_message(f"Loading faces from database: {database_dir}")
    file_count = 0
    loaded_count = 0
    
    for filename in os.listdir(database_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_count += 1
            username = os.path.splitext(filename)[0]
            image_path = os.path.join(database_dir, filename)
            try:
                image = face_recognition.load_image_file(image_path)
                if image.shape[2] != 3:
                    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
                
                face_locations = face_recognition.face_locations(image)
                
                if len(face_locations) == 1:
                    face_encoding = face_recognition.face_encodings(image, face_locations)[0]
                    
                    if isinstance(face_encoding, np.ndarray) and len(face_encoding) == 128:
                        known_faces[username] = face_encoding
                        loaded_count += 1
                        log_message(f"Successfully loaded: {username}")
                    else:
                        log_message(f"Warning: {filename} produced invalid encoding")
                else:
                    log_message(f"Warning: {filename} has {len(face_locations)} faces; skipping.")
            except Exception as e:
                log_message(f"Error loading {filename}: {str(e)}")
    
    log_message(f"Loaded {loaded_count} of {file_count} face(s) from database")
    return known_faces

# Load known faces at startup
KNOWN_FACES = load_known_faces()

# Function to start the voting process with face recognition
def start_voting(username):
    log_message(f"Attempting authentication for username: {username}")
    
    if not username:
        log_message("Error: Username field is empty")
        messagebox.showerror("Error", "Please enter a username.")
        return
    
    if username not in KNOWN_FACES:
        log_message(f"Error: Username '{username}' not found in database")
        messagebox.showerror("Error", f"Username '{username}' not found in the database.")
        return

    for i in range(3):
        ret, frame = cap.read()
        if not ret:
            log_message("Error: Failed to capture image from webcam")
            continue
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        try:
            face_locations = face_recognition.face_locations(rgb_frame)
            log_message(f"Detected {len(face_locations)} face(s) in camera")

            if len(face_locations) != 1:
                if i == 2:
                    log_message("Error: Need exactly one face visible for authentication")
                    messagebox.showerror("Error", "Please ensure only one face is visible.")
                continue

            try:
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                if not face_encodings:
                    log_message("Error: Could not compute face encoding")
                    continue
                    
                face_encoding = face_encodings[0]
                stored_encoding = KNOWN_FACES[username]

                log_message("Comparing face with stored template...")
                match = face_recognition.compare_faces([stored_encoding], face_encoding, tolerance=0.6)[0]
                distance = face_recognition.face_distance([stored_encoding], face_encoding)[0]
                log_message(f"Face match result: {match}, confidence distance: {distance:.4f}")

                if match:
                    log_message("Authentication successful!")
                    messagebox.showinfo("Success", "Face authentication successful. You can now vote!")
                    try:
                        from voting import launch_voting
                        launch_voting(username)
                    except Exception as e:
                        messagebox.showerror("Error", f"An error occurred: {e}") 
                else:
                    log_message("Authentication failed: Face does not match stored user")
                    messagebox.showerror("Authentication Failed", "Face does not match the registered user.")
                
                break
                
            except Exception as e:
                log_message(f"Error during face encoding: {str(e)}")
                if i == 2:
                    messagebox.showerror("Error", "Failed to process face. Please try again.")
                
        except Exception as e:
            log_message(f"Error during face detection: {str(e)}")
            if i == 2:
                messagebox.showerror("Error", f"Face detection error: {str(e)}")
    
# Function to stop the voting process
def stop_voting():
    log_message("Stopping face recognition and closing application")
    messagebox.showinfo("Voting Stopped", "Face recognition stopped. Thank you for using the E-Voting Portal.")
    cap.release()
    root.quit()

# Function to register a new face
def register_new_face():
    username = username_entry.get().strip()
    if not username:
        log_message("Error: Username field is empty")
        messagebox.showerror("Error", "Please enter a username.")
        return
    
    database_dir = "database"
    if not os.path.exists(database_dir):
        os.makedirs(database_dir)
    
    log_message(f"Attempting to register new face for: {username}")
    
    face_detected = False
    for i in range(5):
        ret, frame = cap.read()
        if not ret:
            log_message("Error: Failed to capture image from webcam")
            continue
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        try:
            face_locations = face_recognition.face_locations(rgb_frame)
            
            if len(face_locations) == 1:
                face_detected = True
                break
            else:
                root.update()
                root.after(300)
        except Exception as e:
            log_message(f"Error during face detection: {str(e)}")
    
    if not face_detected:
        log_message("Failed to detect exactly one face for registration")
        messagebox.showerror("Error", "Please ensure only one face is visible.")
        return
    
    file_path = os.path.join(database_dir, f"{username}.jpg")
    cv2.imwrite(file_path, frame)
    
    try:
        test_image = face_recognition.load_image_file(file_path)
        test_face_locations = face_recognition.face_locations(test_image)
        
        if len(test_face_locations) == 1:
            test_face_encoding = face_recognition.face_encodings(test_image, test_face_locations)[0]
            
            global KNOWN_FACES
            KNOWN_FACES[username] = test_face_encoding
            
            log_message(f"Successfully registered face for: {username}")
            messagebox.showinfo("Registration Successful", f"Face for '{username}' has been registered.")
            update_available_users()
        else:
            log_message(f"Verification failed: Saved image has {len(test_face_locations)} faces")
            messagebox.showerror("Registration Failed", "Could not verify the saved face image. Please try again with better lighting.")
    except Exception as e:
        log_message(f"Error verifying registered face: {str(e)}")
        messagebox.showerror("Registration Error", f"An error occurred during registration: {e}")

def update_available_users():
    available_users = ", ".join(KNOWN_FACES.keys()) if KNOWN_FACES else "None"
    users_text.config(text=available_users)

# Function to build the GUI dynamically
def build_gui():
    global username_entry, users_text
    
    header_frame = tk.Frame(root, bg="#4a86e8", height=60)
    header_frame.pack(fill=tk.X)
    
    header_label = tk.Label(header_frame, text="E-Voting Portal - Face Authentication", 
                           font=("Helvetica", 18, "bold"), bg="#4a86e8", fg="white", padx=20, pady=10)
    header_label.pack()

    instructions = tk.Label(root, text="Please position your face in front of the camera for authentication.", 
                            font=("Helvetica", 14), bg="#f5f5f5", wraplength=750)
    instructions.pack(pady=10)

    status_label = tk.Label(root, textvariable=status_text, font=("Helvetica", 12), bg="#f5f5f5")
    status_label.pack(pady=10)

    username_frame = tk.Frame(root, bg="#f5f5f5")
    username_frame.pack(pady=5)
    
    username_label = tk.Label(username_frame, text="Enter Username:", font=("Helvetica", 12), bg="#f5f5f5")
    username_label.pack(side=tk.LEFT, padx=5)
    
    username_entry = tk.Entry(username_frame, font=("Helvetica", 12), bg="white", width=20)
    username_entry.pack(side=tk.LEFT, padx=5)

    button_frame = tk.Frame(root, bg="#f5f5f5")
    button_frame.pack(pady=10)

    start_button = tk.Button(button_frame, text="Start Voting", font=("Helvetica", 12), bg="#4CAF50", fg="white",
                            command=lambda: start_voting(username_entry.get().strip()), width=12)
    start_button.grid(row=0, column=0, padx=10)

    register_button = tk.Button(button_frame, text="Register Face", font=("Helvetica", 12), bg="#2196F3", fg="white",
                               command=register_new_face, width=12)
    register_button.grid(row=0, column=1, padx=10)

    stop_button = tk.Button(button_frame, text="Stop", font=("Helvetica", 12), bg="#f44336", fg="white",
                           command=stop_voting, width=12)
    stop_button.grid(row=0, column=2, padx=10)

    users_frame = tk.Frame(root, bg="#f5f5f5")
    users_frame.pack(pady=5)
    
    users_label = tk.Label(users_frame, text="Available Users:", font=("Helvetica", 10, "bold"), bg="#f5f5f5")
    users_label.pack(side=tk.LEFT, padx=5)
    
    available_users = ", ".join(KNOWN_FACES.keys()) if KNOWN_FACES else "None"
    users_text = tk.Label(users_frame, text=available_users, font=("Helvetica", 10), bg="#f5f5f5")
    users_text.pack(side=tk.LEFT, padx=5)

    video_frame = tk.Frame(root, bg="#eeeeee", bd=2, relief=tk.SUNKEN)
    video_frame.pack(pady=10)
    
    panel = tk.Label(video_frame, bd=0)
    panel.pack(padx=5, pady=5)

    def update_frame_content():
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                try:
                    face_locations = face_recognition.face_locations(rgb_frame)

                    for (top, right, bottom, left) in face_locations:
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                        cv2.putText(frame, f"Face #{face_locations.index((top, right, bottom, left))+1}", 
                                    (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame_rgb)
                    img = img.resize((640, 480), Image.LANCZOS)
                    img_tk = ImageTk.PhotoImage(img)
                    
                    panel.config(image=img_tk)
                    panel.image = img_tk

                    if len(face_locations) > 0:
                        status_text.set(f"Status: {len(face_locations)} face(s) detected! Ready for authentication.")
                    else:
                        status_text.set("Status: No face detected. Please position your face.")
                except Exception as e:
                    log_message(f"Error updating frame: {str(e)}")

        root.after(100, update_frame_content)

    update_frame_content()

# Check for required modules
try:
    modules = ["cv2", "PIL", "face_recognition"]
    missing_modules = []
    
    for module in modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        messagebox.showerror("Missing Modules", f"Missing required modules: {', '.join(missing_modules)}\n\nPlease install them using pip.")
        sys.exit(1)
    
    if not os.path.exists("voting.py"):
        pass
        
except Exception as e:
    messagebox.showerror("Error", f"Initialization error: {str(e)}")
    sys.exit(1)

# Start the application
build_gui()
root.protocol("WM_DELETE_WINDOW", stop_voting)
root.mainloop()

if 'cap' in locals() and cap.isOpened():
    cap.release()