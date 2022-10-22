import database.db_connect


def checkUser(userID):
    (conn, cur) = db_connect.connectDatabase()
    cur.execute('SELECT * FROM User WHERE id = ?', (userID,))
    result = cur.fetchone()
    return (result != None)


def checkBook(bookID):
    (conn, cur) = db_connect.connectDatabase()
    cur.execute('SELECT * FROM Book WHERE id = ?', (bookID,))
    result = cur.fetchone()
    return (result != None)
