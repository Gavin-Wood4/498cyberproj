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

