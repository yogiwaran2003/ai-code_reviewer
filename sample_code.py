import os
import sqlite3

# Sample user login function - intentionally has some issues for review demo
def login(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Vulnerable to SQL injection
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()

    if user:
        return True
    return False


def get_all_passwords():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users")
    return cursor.fetchall()


def calculate_discount(price, discount):
    # No validation on inputs
    return price - (price * discount / 100)


def read_file(filepath):
    f = open(filepath, "r")
    content = f.read()
    # File never closed
    return content
