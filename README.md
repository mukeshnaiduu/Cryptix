# 🔐 Cryptix – Every Word is a Mystery  
A Flask-based word-guessing game inspired by Wordle, with **player and admin roles**, daily game limits, and detailed reports.  

---

## 📌 Features  

### 👤 Player  
- Register and log in (secure authentication with validation).  
- Play up to **3 games per day**; each game allows **5 guesses** of 5-letter uppercase words.  
- Get interactive feedback on every guess:  
  - 🟩 **Green** – correct letter, correct position.  
  - 🟧 **Orange** – correct letter, wrong position.  
  - ⬛ **Grey** – letter not in the word.  
- Win with a celebratory banner or see a “Better luck next time” message after 5 attempts.  
- Review previous guesses in-order while playing.  

### 🛠️ Admin  
- Log in to access dashboards and reports (admin accounts don’t play the guessing game).  
- View the **daily report** (players who played, wins) for any date.  
- Inspect detailed **per-player reports** with win/loss counts, total guesses, averages, and full game history.  
- Seed and manage the initial 20-word bank via CLI tools.  

---

## 🗄️ Tech Stack  
- **Backend:** Flask (Python)  
- **Frontend:** HTML, CSS (Bootstrap 5), JavaScript  
- **Database:** SQLite (development default)  
- **ORM:** SQLAlchemy  
- **Auth:** Flask-Login, Bcrypt for password hashing  

---

## 🏗️ Project Structure  
```

cryptix/
│── app.py              # Flask app entry point
│── app/
│    ├── __init__.py    # Application factory
│    ├── cli.py         # Flask CLI commands (init-db, seed-words, create-admin)
│    ├── extensions.py  # Flask extensions (db, login, migrate, bcrypt)
│    ├── models.py      # Database models (Users, Words, Games, Guesses)
│    ├── routes/        # Flask Blueprints (auth, game, admin)
│    └── seeds.py       # Default word list for seeding
│── templates/
│    ├── base.html
│    ├── dashboard.html
│    ├── game.html
│    ├── login.html
│    ├── register.html
│    └── admin/
│         ├── dashboard.html
│         ├── daily_report.html
│         ├── players.html
│         └── user_report.html
│── static/
│    ├── css/main.css
│    └── js/main.js
│── requirements.txt
│── README.md

````

---

## 🚀 Getting Started  

### 1. Clone the repository  
```bash
git clone https://github.com/mukeshnaiduu/Cryptix.git
cd Cryptix
````

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux  
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize the database and seed words

```bash
flask --app app init-db
```

> Need to refresh the word list later? Run `flask --app app seed-words --force`.

> Optional: create an admin user quickly

```bash
flask --app app create-admin <username> <password>
```

### 5. Run the app

```bash
flask run
```

The app will be available at 👉 `http://127.0.0.1:5000`

---

## 🔧 CLI quick reference

```bash
flask --app app init-db                 # Create tables and seed the default 20 words
flask --app app seed-words --force      # Reseed word list (clears and reloads defaults)
flask --app app create-admin alice P@ss1 # Create an admin with username/password
```
