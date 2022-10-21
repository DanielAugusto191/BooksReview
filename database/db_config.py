import db_system
import sqlite3
connection = sqlite3.connect("database/database.db")
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

# db_system.updateUsername(1, "sasa")
# db_system.setReview(1, "TESTE", "TESTE@")

with open("database/db_config.sql") as f:
    connection.executescript(f.read())