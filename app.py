from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create database
def create_database():
    conn = sqlite3.connect("event.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

create_database()

# Home Page
@app.route('/')
def home():
    return render_template("index.html")

# Student Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("event.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO students(name,email,password) VALUES(?,?,?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template("student_register.html")

# Student Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("event.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM students WHERE email=? AND password=?",
            (email, password)
        )

        user = cur.fetchone()

        conn.close()

        if user:
            return redirect('/events')
        else:
            return "Invalid Login"

    return render_template("student_login.html")

# Admin Login
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin123":
            return "<h2>Welcome Admin</h2><a href='/'>Home</a>"
        else:
            return "Invalid Admin Login"

    return render_template("admin_login.html")

# Events Page
@app.route('/events')
def events():
    return render_template("events.html")

if __name__ == "__main__":
    app.run(debug=True)