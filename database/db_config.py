import sqlite3
connection = sqlite3.connect("database/database.db")
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

with open("database/db_config.sql") as f:
    connection.executescript(f.read())