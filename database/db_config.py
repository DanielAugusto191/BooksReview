import sqlite3
connection = sqlite3.connect("database.db")
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

with open("db_config.sql") as f:
    connection.executescript(f.read())