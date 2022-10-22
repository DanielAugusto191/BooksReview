from database.db_connect import connectDatabase


def checkUser(userID):
    (conn, cur) = connectDatabase()
    cur.execute('SELECT * FROM User WHERE id = ?', (userID,))
    result = cur.fetchone()
    return (result != None)


def checkBook(bookID):
    (conn, cur) = connectDatabase()
    cur.execute('SELECT * FROM Book WHERE id = ?', (bookID,))
    result = cur.fetchone()
    return (result != None)

def checkStatus(status):
    return (status < 0 or status > 3)
        