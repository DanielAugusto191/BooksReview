import sqlite3

def connectDatabase():
    conn = sqlite3.connect("database/database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return (conn, cur)
