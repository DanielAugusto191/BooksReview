# Aqui vai ter request ao banco para profiles.
import sqlite3

def userInfo(id):
    works = False
    msg = ""
    account = ""
    try:
        conn = sqlite3.connect("database/database.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('SELECT * FROM User WHERE id = ?', (id,))
        account = cur.fetchone()
        works = True
    except Exception as e:
        msg = e
    return (works, msg, account)