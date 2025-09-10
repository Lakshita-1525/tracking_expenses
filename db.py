import sqlite3
import pandas as pd

def init_db():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_expense(date, category, amount, description):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
              (date, category, amount, description))
    conn.commit()
    conn.close()

def fetch_expenses():
    conn = sqlite3.connect("expenses.db")
    df = pd.read_sql("SELECT * FROM expenses", conn, parse_dates=["date"])
    conn.close()
    return df
