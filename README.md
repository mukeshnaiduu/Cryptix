# 🔐 Cryptix – Every Word is a Mystery  
A Flask-based word-guessing game inspired by Wordle, with **player and admin roles**, daily game limits, and detailed reports.  

---

## 📌 Features  

### 👤 Player  
- Register and log in (secure authentication with validation).  
- Play up to **3 games per day**.  
- Each game allows **5 guesses** to crack a random 5-letter word.  
- Interactive feedback for guesses:  
  - 🟩 **Green** – correct letter, correct position.  
  - 🟧 **Orange** – correct letter, wrong position.  
  - ⬛ **Grey** – letter not in the word.  
- Win with a congratulatory message 🎉 or see a “Better luck next time” message.  
- Past guesses shown in sequence.  

### 🛠️ Admin  
- Manage the word bank (20+ 5-letter words stored in DB).  
- View **daily reports**: number of users, number of correct guesses.  
- View **user reports**: date, number of games played, number of correct guesses.  

---

## 🗄️ Tech Stack  
- **Backend:** Flask (Python)  
- **Frontend:** HTML, CSS (Bootstrap/Tailwind), JavaScript  
- **Database:** SQLite (default) – can be swapped for PostgreSQL/MySQL  
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
│    ├── routes/        # Flask Blueprints
│    │    ├── auth.py   # User authentication routes
│    │    ├── game.py   # Game play logic
│    │    └── admin.py  # Admin routes & reports
│    └── seeds.py       # Default word list for seeding
│── templates/          # HTML templates (Jinja2)
│    ├── base.html
│    ├── login.html
│    ├── register.html
│    ├── dashboard.html
│    ├── game.html
│    └── reports.html
│── static/             # Static files
│    ├── css/
│    ├── js/
│── static/             # CSS/JS assets
│── requirements.txt    # Dependencies
│── README.md           # Project description

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

## 📦 Requirements

Example `requirements.txt`:

```
Flask==2.3.3
Flask-Login==0.6.3
Flask-SQLAlchemy==3.1.1
Flask-Bcrypt==1.0.1
Flask-Migrate==4.0.7
python-dotenv==1.0.1
```

---

## 📜 License

This project is licensed under the MIT License. Feel free to use and modify.
