# 🗳️ E-Voting Portal (Python Version)

A secure, modern, and inclusive **Python-based E-Voting System** built as a **SE Mini Project (SEM 5)** for the Bachelor of Engineering (Information Technology) degree at **Thadomal Shahani Engineering College**, University of Mumbai.

This project reimagines the voting process by leveraging **Python (Tkinter, Flask)** and **SQLite**, offering features like face recognition, graphical result analysis, and real-time election control to enhance accessibility, trust, and security.

---

## 🚀 Key Features

### 🔐 Secure Login System
- Role-based login: **Voter**, **Admin**, and **Super Admin**
- CAPTCHA integration for bot prevention
- Optional **Face Recognition** using OpenCV for biometric login
- Multi-factor authentication with security questions

### 🧑‍⚖️ Admin Controls
- Real-time vote monitoring
- Pause/Terminate elections during runtime
- View & download voter list
- Manage election status securely

### 🗳️ Voter Dashboard
- Cast vote via intuitive UI
- Countdown-based voting window
- Vote confirmation prompts
- Feedback form post-voting
- OTP or Twilio integration for vote acknowledgment (optional)

### 📊 Results & Visualization
- Real-time vote tallying
- Results shown with **pie charts** and **bar graphs** using Matplotlib
- Final results are **immutable** and auditable
- Option to export/download results

### 🏛️ Super Admin Panel
- Full administrative access
- Officially declare results
- Manage system-wide integrity checks and audit trails

### 📰 Additional Features
- Live election news feed with multilingual support
- Notifications via Twilio (SMS) after vote submission

---

## 🏗️ Architecture

- **Frontend/UI:** Tkinter (Python GUI)
- **Backend Logic:** Python (core + Flask for integrations)
- **Database:** SQLite3 (or MySQL, modular support)
- **Authentication:** Password, CAPTCHA, Face Recognition
- **Visualization:** Matplotlib, Seaborn (for results and stats)

---

## 🔄 User Flow

1. **Login**
   - User/Admin/Super Admin login via credentials, CAPTCHA, and optionally face recognition

2. **Voting**
   - Voter selects party, confirms ballot, and submits

3. **Election Monitoring**
   - Admin tracks votes, voter status, and can pause/end elections

4. **Feedback Collection**
   - Voters submit post-vote feedback

5. **Result Declaration**
   - System auto-generates graphical results and locks them

---

## 🧪 Technologies Used

| Component            | Technology         |
|---------------------|--------------------|
| GUI Framework        | Python Tkinter     |
| Backend Logic        | Python, Flask      |
| Database             | SQLite3 / MySQL    |
| Visualizations       | Matplotlib, Seaborn|
| Authentication       | CAPTCHA, Face Auth |
| Notifications        | Twilio API (SMS)   |
| AI Integration       | OpenCV             |

---

📄 _The full mini project report is also available in this repository as_ **evotingreportfinal.pdf**.

