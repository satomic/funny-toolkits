#coding=utf-8
import sqlite3


if __name__ == "__main__":
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
    conn.close()
