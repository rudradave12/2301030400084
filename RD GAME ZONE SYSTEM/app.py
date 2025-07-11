from flask import Flask, render_template, request, redirect
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Create DB and table
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        in_time TEXT,
        out_time TEXT,
        duration REAL,
        amount INTEGER,
        games TEXT,
        platform TEXT,
        tv_size TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM customers")
    records = c.fetchall()
    conn.close()
    return render_template('index.html', records=records)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    in_time = request.form['in_time']
    out_time = request.form['out_time']
    games = request.form['games']
    platform = request.form['platform']
    tv_size = request.form['tv_size']

    fmt = "%H:%M"
    duration = (datetime.strptime(out_time, fmt) - datetime.strptime(in_time, fmt)).seconds / 3600
    amount = int(duration * 100)  # ₹100 per hour

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO customers (name, in_time, out_time, duration, amount, games, platform, tv_size) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (name, in_time, out_time, duration, amount, games, platform, tv_size))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)