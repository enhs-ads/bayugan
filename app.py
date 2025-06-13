from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecret'  # Needed for session management

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return redirect(url_for('login'))  # Always redirect to login

@app.route('/mainpage')
def mainpage():
    if 'user' in session:
        return render_template('mainpage.html')  # Your main page
    return redirect(url_for('login'))  # Block access if not logged in

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (uname, pwd))
        user = cur.fetchone()
        conn.close()
        if user:
            session['user'] = uname
            return redirect(url_for('mainpage'))
        else:
            return "Invalid username or password"
    return render_template('login.html')

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')  # Shows options for manual/google/facebook

@app.route('/register/manual', methods=['GET', 'POST'])
def register_manual():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (uname, pwd))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Username already taken"
        conn.close()
        return redirect(url_for('login'))
    return render_template('manual_register.html')

@app.route('/register/google', methods=['GET', 'POST'])
def register_google():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (email, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "email already used"
        conn.close()
        return redirect(url_for('login'))
    return render_template('google_register.html')

@app.route('/register/facebook', methods=['GET', 'POST'])
def register_facebook():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (email, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "email already used"
        conn.close()
        return redirect(url_for('login'))
    return render_template('facebook_register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/card1')
def card1():
    return render_template('card1.html')

@app.route('/kk')
def kk():
    return render_template('kk.html')

@app.route('/show-users')
def show_users():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    conn.close()
    return render_template('users.html', users=users)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
