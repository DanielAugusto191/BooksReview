# Esse arquivo é só para testar o banco de dados sem alterar as funções

import db_system
import sqlite3
connection = sqlite3.connect("database/database.db")
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

# cursor.execute("INSERT INTO Book (id, title, cover, description, rate) VALUES (?, ?, ?, ?, ?)", ('maça', 'test', 'copa', 'descrição2', '2.0'))
# connection.commit()
# db_system.updateUsername(1, "sasa")
# a = db_system.setReview(1, "TESTE2", "TESTE!")
# a = db_system.userInfo(1)
# a = db_system.setReview(1, "maça", "Teste de Review maça!")
# a = db_system.updateReview(1, "limao", "Review Atualizado")
# a = db_system.getReview(1, "limao")
# a = db_system.getAllReviews(1)
a = db_system.delRate(1, "limao")
print(a)

# with open("database/db_config.sql") as f:
#     connection.executescript(f.read())