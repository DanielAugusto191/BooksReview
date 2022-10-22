# Aqui vai ter request ao banco.
# from sys import path
# path.insert(0, "/home/pc2/facul/sem8/ES/BooksReview/")

import datetime
from database.db_checks import *
from database.db_connect import *
from Book import Book
"""
Summary:
#Users
    userInfo(id) - Given a user id return yours info.
    updatePassword(id, oldPassword, newPassword) -  Update user's password
    updateProfilePicture(id, newProfilePicture) - Update user's profile picture
    updateUsername(id, newUserName) - Update user's username

#Books
    addBook(book) - Given a book object, add it in Database.
    getBookByID(bookID) - Given a book ID return a object of Book, with all informations in Database.
    updateBookRate(bookID) - Given a book ID, update the rate of this book, the rate is equal to the mean of all user's rate, rounded.

#Review
    setReview(userID, bookID, review) - Set a new review of a book
    updateReview(userID, bookID, review) - Update a review of a book
    getReview(userID, bookID) - Get a User's review of a book
    getAllReviews(userID) - Get all reviews of a User
    delReview(userID, book) - Delete a review of a user.

#Rate
    setRate(userID, bookID, rate) - Assigns the rate the user has given to a book
    updateRate(userID, bookID, newRate) - Update the rate the user has given to a book
    getRate(userID, book) - Get the rate that user given to the book. 
    getAllRate(userID) - Get all the rates given by the user.
    delRate(userID, book) - Delete a rate given to a book.

#Status
    setStatus(userID, book, status) - Assigns the book status. (0 = Unreaded, 1 = Want to read, 2 = Reading, 3 = Complete)
    getStatus(userID, book) - Get status of a user about the book.
    getAllStatus(userID) - Get all user's status.
    delStatus(userID, book) - Delete user's status of a book.

#Favorite
    toogleBookAsFavorite(UserID, bookID) - Set/Unset a book as users favorite. (Limit of 5 books)
    requestFavoritesBooks(UserID, bookID) - Return the users favorite books

Parameters and Return are given below:
"""
### USER ####

def userInfo(id):
    ''' 
Given a user id return yours info.

Parametes:
id = User ID

Return:
tuple of:
    works = True/False - If there is no error.
    msg = ""/"{error}" - Empty if works, or return the error
    account = Dict with accout infos:
        - ID = User id
        - Username = User's username
        - Email = user's Email
'''
    works = False
    msg = ""
    account = ""
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(id):
            raise Exception("Invalid UserID!")
        cur.execute('SELECT * FROM User WHERE id = ?', (id,))
        account = cur.fetchone()
        if account == None:
            raise Exception("ID invalido!")
        account = dict(account)
        del account["password"]
        print(account)
        works = True
    except Exception as e:
        msg = e
    return (works, msg, account)

def updatePassword(id, oldPassword, newPassword):
    ''' 
Update user's password

Parameters:
id = User id
oldPassword = String with the User's Old Password to confirm
newPassword = String with the User's New Password to set as the new Password

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = "Update com sucesso!"/"{error}" - Status of works.
'''
    works = False
    msg = ""
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(id):
            raise Exception("Invalid UserID!")
        cur.execute('SELECT password FROM User WHERE id = ?', (id,))
        result = cur.fetchone()
        if result == None:
            raise Exception("ID invalido!")
        result = dict(result)
        if oldPassword == result["password"]:
            cur.execute("UPDATE User SET password = ? WHERE id = ?", (newPassword, id,))
            conn.commit()
        works = True
        msg = "Update com sucesso!"
    except Exception as e:
        msg = e
    return (works, msg)

def updateProfilePicture(id, newProfilePicture):
    ''' 
Update user's profile picture

Parameters:
id = User id
newProfilePicture = data for set new profile picture

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = ""/"{error}" - Status of works.
'''
    pass

def updateUsername(id, newUserName):
    ''' 
Update user's username

Parameters:
id = User id
newUserName = New username to update.

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = ""/"{error}" - Status of works.
'''
    works = False
    msg = ""
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(id):
            raise Exception("Invalid UserID!")
        cur.execute("UPDATE User SET username = ? WHERE id = ?", (newUserName, id,))
        conn.commit()
        works = True
        msg = "Update com sucesso!"
    except Exception as e:
        msg = e
    return (works, msg)

### BOOKS ###

def addBook(book):
    ''' 
Given a book object, add it in Database.

Parameters:
book: book Object

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = "Livro adicionado!"/"{error}" - Status of works.
'''
    works = False
    msg = ""
    try:
        (conn, cur) = connectDatabase()
        if checkBook(book.id):
            raise Exception("Books already in DB")
        # TODO: bookRate
        cur.execute("INSERT INTO Book (id, title, cover, author, description, rate) VALUES (?, ?, ?, ?, ?, ?)", (book.id, book.title, book.imageLink, book.authors[0], book.description, 0.0))
        conn.commit()
        works = True
        msg = "Livro adicionado!"
    except Exception as e:
        msg = e
    return (works, msg)

def getBookByID(bookID):
    ''' 
Given a book ID return a object of Book, with all informations in Database.

Parameters:
bookID: ID of a book;

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = "ok"/"{error}" - Status of works.
    Book = Object of type book, with all informations in Database.
'''
    works = False
    msg = ""
    book = None
    try:
        (conn, cur) = connectDatabase()
        if not checkBook(bookID):
            raise Exception("Books not in DB")
        cur.execute("SELECT * from Book WHERE id = ?", (bookID,))
        result = cur.fetchone()
        if result == None:
            raise Exception("No book with this ID")
        result = dict(result)
        bb = {"id": result["id"], "volumeInfo": {"title": result["title"], "authors": result["author"], "description": result["description"], "imageLinks": {"smallThumbnail": result["cover"]}}}
        book = Book(bb)
        works = True
        msg = "ok"
    except Exception as e:
        msg = e
    return (works, msg)

def updateBookRate(bookID):
    ''' 
Given a book ID, update the rate of this book, the rate is equal to the mean of all user's rate, rounded.

Parameters:
bookID: ID of a book;

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = "ok"/"{error}" - Status of works.
'''
    works = False
    msg = ""
    try:
        (conn, cur) = connectDatabase()
        if not checkBook(bookID):
            raise Exception("Books not in DB")
        cur.execute("SELECT rate from rate WHERE fk_Book = ?", (bookID,))
        result = cur.fetchall()
        n = 0
        s = 0
        for e in result:
            n += 1
            s += e['rate']
        new_rate = round(s/n, 1)
        cur.execute("UPDATE book SET rate = ? WHERE id = ?", (new_rate, bookID,))
        conn.commit()
        works = True
        msg = "ok"
    except Exception as e:
        msg = e
    return (works, msg)

### REVIEW ####
def setReview(userID, book, review):
    ''' 
Set a new review of a book

Parameters:
userID = User id
bookObject = book Object
Review = String with the user review.

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = ""/"{error}" - Status of works.
    result = None,{review_id, data} - if works return nothing, if not return a dict with previous review_id and date of review.
'''
    works = False
    msg = ""
    result = None
    bookID = book.id
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        if not checkBook(bookID):
            addBook(book)
        cur.execute('SELECT id, date FROM Review WHERE fk_User = ? and fk_Book = ?', (userID, bookID))
        result = cur.fetchone()
        if result == None:
            cur.execute("INSERT INTO Review (fk_User, fk_Book, review, date) VALUES (?, ?, ?, ?)", (userID, bookID,  review, datetime.datetime.now()))
            conn.commit()
            works = True
            msg = "Review adicionado!"
        else:
            result = dict(result)
            if result:
                msg = ("Você ja fez um review sobre esse livro!" )
    except Exception as e:
        msg = e
    return (works, msg, result)

def updateReview(userID, book, review):
    ''' 
Update a review of a book

Parameters:
userID = User id
book = book Object
Review = String with the new user review.

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = ""/"{error}" - Status of works.
'''
    works = False
    msg = ""
    bookID = book.id
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        if not checkBook(bookID):
            addBook(book)
        cur.execute("UPDATE Review SET review = ? WHERE fk_User = ? and fk_Book = ?", (review, userID, bookID,))
        conn.commit()
        works = True
    except Exception as e:
        msg = e
    return (works, msg)


def getReview(userID, book):
    ''' 
Get a User's review of a book

Parameters:
userID = User id
book = book Object

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = ""/"{error}" - Status of works.
    review = Users review (that are Dicts of Date and Review) - {"date"=2022-01-022 10:37:35.123456, "review"=Review}
'''
    works = False
    msg = ""
    review = ""
    bookID = book.id
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        if not checkBook(bookID):
            addBook(book)
        cur.execute("SELECT date, review FROM Review WHERE fk_User = ? and fk_Book = ?", (userID, bookID,))
        result = cur.fetchone()
        if result == None:
            raise Exception("Reviews not found!")
        review = dict(result)
        works = True
        msg = ""
    except Exception as e:
        msg = e
    return (works, msg, review)

def getAllReviews(userID):
    ''' 
Get all reviews of a User

Parameters:
userID = User id

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = ""/"error" - Status of works.
    reviews = List of Reviews(that are Dicts of Books ID, Books name, rate and Review) - [{"BookID"=ID, "BookName"=BooksName,"rate"=rate, "review"=Review}, {"BookID"=ID, "BookName"=BooksName, "rate"=rate, "review"=Review}, ...]
'''
    works = False
    msg = ""
    review = []
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        cur.execute("SELECT date, review, fk_Book FROM Review WHERE fk_User = ?", (userID,))
        result = cur.fetchall()
        for e in result:
            review.append(dict(e))
        if len(result) == 0:
            raise Exception("Wrong ID or Reviews not found!")
        works = True
        msg = ""
    except Exception as e:
        msg = e
    return (works, msg, review)

# Delete o review
def delReview(userID, book):
    ''' 
Delete a review of a user.

Parameters:
userID = User id
book = book Object

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = ""/"error" - Status of works.
'''
    works = False
    msg = ""
    bookID = book.id
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        if not checkBook(bookID):
            addBook(book)
        cur.execute("DELETE FROM review WHERE fk_User = ? and fk_Book = ?", (userID, bookID))
        conn.commit()
        works = True
        msg = ""
    except Exception as e:
        msg = e
    return (works, msg)

### RATE ####

def setRate(userID, book, rate):
    ''' 
Assigns the rate the user has given to a book

Parameters:
userID = User id
book = book Object
rate = The rate that user gives to the book.

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = ""/"{error}" - Status of works.
    result = None,{rate_id, data} - if works return nothing, if not return a dict with previous rate_id and date of rate.
'''
    works = False
    msg = ""
    result = None
    bookID = book.id
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        if not checkBook(bookID):
            addBook(book)

        cur.execute('SELECT id, date FROM Rate WHERE fk_User = ? and fk_Book = ?', (userID, bookID))
        result = cur.fetchone()
        if result == None:
            cur.execute("INSERT INTO Rate (fk_User, fk_Book, rate, date) VALUES (?, ?, ?, ?)", (userID, bookID,  rate, datetime.datetime.now()))
            conn.commit()
            works = True
            msg = "Rate adicionado!"
            updateBookRate(bookID)
        else:
            result = dict(result)
            if result:
                msg = ("Você ja deu uma nota para esse livro!" )
    except Exception as e:
        msg = e
    return (works, msg, result)
    pass

def updateRate(userID, book, newRate):
    ''' 
Update the rate the user has given to a book

Parameters:
userID = User id
book = book Object
newRate = The rate that user gives to the book.

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = ""/"{error}" - Status of works.
'''
    works = False
    msg = ""
    bookID = book.id
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        if not checkBook(bookID):
            addBook(book)
        cur.execute("UPDATE rate SET rate = ? WHERE fk_User = ? and fk_Book = ?", (newRate, userID, bookID,))
        conn.commit()
        updateBookRate(bookID)
        works = True
    except Exception as e:
        msg = e
    return (works, msg)

def getRate(userID, book):
    ''' 
Get the rate that user given to the book.

Parameters:
userID = User id
book = book Object

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = ""/"{error}" - Status of works.
    result = {rate} - Rate given to the book.
'''
    works = False
    msg = ""
    result = None
    bookID = book.id
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        if not checkBook(bookID):
            addBook(book)
        cur.execute("SELECT date, rate FROM rate WHERE fk_User = ? and fk_Book = ?", (userID, bookID,))
        result = cur.fetchone()
        if result == None:
            raise Exception("Rate not found!")
        result = dict(result)
        works = True
        msg = ""
    except Exception as e:
        msg = e
    return (works, msg, result)

def getAllRate(userID):
    ''' 
Get all the rates given by the user.

Parameters:
userID = User id

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = ""/"{error}" - Status of works.
    rates = [{"data":"data", "rate":"rate", "fk_Book":"bookID"},...] - List of dict(data, rate and bookID);
'''
    works = False
    msg = ""
    rates = []
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        cur.execute("SELECT date, rate, fk_Book FROM rate WHERE fk_User = ?", (userID,))
        result = cur.fetchall()
        for e in result:
            rates.append(dict(e))
        if len(rates) == 0:
            raise Exception("Rate not found!")
        works = True
        msg = ""
    except Exception as e:
        msg = e
    return (works, msg, rates)

def delRate(userID, book):
    ''' 
Get all the rates given by the user.

Parameters:
userID = User id
book = book Object

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = ""/"{error}" - Status of works.
'''
    works = False
    msg = ""
    bookID = book.id
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        if not checkBook(bookID):
            addBook(book)
        cur.execute("DELETE FROM rate WHERE fk_User = ? and fk_Book = ?", (userID, bookID))
        conn.commit()
        works = True
        msg = ""
    except Exception as e:
        msg = e
    return (works, msg)

### STATUS ####
# (0 = Unreaded, 1 = Want to read, 2 = Reading, 3 = Complete)

def setStatus(userID, book, status):
    ''' 
Assigns the book status. (0 = Unreaded, 1 = Want to read, 2 = Reading, 3 = Complete)

Parameters:
userID = User id
book = book Object
status = (0 = Unreaded, 1 = Want to read, 2 = Reading, 3 = Complete)

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = ""/"{error}" - Status of works.
'''
    works = False
    msg = ""
    bookID = book.id
    try:
        (conn, cur) = connectDatabase()
        if checkStatus(status):
            raise Exception("Invalid Status")
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        if not checkBook(bookID):
            addBook(book)
        cur.execute('SELECT id, date FROM Status WHERE fk_User = ? and fk_Book = ?', (userID, bookID))
        result = cur.fetchone()
        if result == None:
            cur.execute("INSERT INTO Status (fk_User, fk_Book, status, date) VALUES (?, ?, ?, ?)", (userID, bookID,  status, datetime.datetime.now()))
            conn.commit()
            works = True
            msg = "Status adicionado!"
        else:
            cur.execute("UPDATE Status SET Status = ? WHERE fk_User = ? and fk_Book = ?", (status, userID, bookID,))
            conn.commit()
            woks = True
            msg = "Status Atualizado!"
        works = True
    except Exception as e:
        msg = e
    return (works, msg)

def getStatus(userID, book):
    ''' 
Get status of a user about the book.

Parameters:
userID = User id
book = book Object

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = ""/"{error}" - Status of works.
    result = None / {"data": data, "status":INT} - None if dont work, dict(data, status) if works.
'''
    works = False
    msg = ""
    result = None
    bookID = book.id
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        if not checkBook(bookID):
            addBook(book)
        cur.execute("SELECT date, status FROM Status WHERE fk_User = ? and fk_Book = ?", (userID, bookID,))
        result = cur.fetchone()
        if result == None:
            result = {"date": None, "status": 0}
        else:
            result = dict(result)
        works = True
        msg = ""
    except Exception as e:
        msg = e
    return (works, msg, result)

def getAllStatus(userID):
    ''' 
Get all user's status.

Parameters:
userID = User id

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = ""/"{error}" - Status of works.
    status = [] / [{"data": data, "status":INT, "fk_Book":bookID},...] - [] if dont work, list of dict(data, status, fk_Book) if works.
'''
    works = False
    msg = ""
    status = []
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        cur.execute("SELECT date, status, fk_Book FROM status WHERE fk_User = ?", (userID,))
        result = cur.fetchall()
        for e in result:
            status.append(dict(e))
        if len(status) == 0:
            raise Exception("Status not found!")
        works = True
        msg = ""
    except Exception as e:
        msg = e
    return (works, msg, status)

def delStatus(userID, book):
    ''' 
Delete user's status of a book.

Parameters:
userID = User id
book = Book Object

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = ""/"{error}" - Status of works.
'''
    works = False
    bookID = book.id
    msg = ""
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        if not checkBook(bookID):
            addBook(book)
        cur.execute("DELETE FROM status WHERE fk_User = ? and fk_Book = ?", (userID, bookID))
        conn.commit()
        works = True
        msg = ""
    except Exception as e:
        msg = e
    return (works, msg)

### FAVORITES ####
def toogleBookAsFavorite(userID, book):
    ''' 
Set/Unset a book as users favorite.

Parameters:
userID = User id
book = book Object

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = "on/off" / "{error}" - Status of works. on = addde, off = removed
'''
    works = False
    bookID = book.id
    msg = ""
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        if not checkBook(bookID):
            addBook(book)
        cur.execute("SELECT * from Favorites WHERE fk_User = ? and fk_Book = ?", (userID, bookID))
        result = cur.fetchone()
        if result == None:
            cur.execute("INSERT INTO Favorites (fk_User, fk_Book) VALUES(?, ?)", (userID, bookID)) 
            msg = "On"
        else:
            cur.execute("DELETE FROM Favorites WHERE fk_User = ? and fk_Book = ?", (userID, bookID))
            msg = "Off"
        conn.commit()
        works = True
    except Exception as e:
        msg = e
    return (works, msg)

def requestFavoritesBooks(userID):
    ''' 
Return the users favorite books

Parameters:
userID = User id
book = book Object

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = ""/"{error}" - Status of works.
    Books = List of Reviews(that are Dicts of Books ID, Books name, rate and Review) - [{"BookID"=ID, "BookName"=BooksName,"rate"=rate, "review"=Review}, {"BookID"=ID, "BookName"=BooksName, "rate"=rate, "review"=Review}, ...]
'''
    works = False
    msg = ""
    bookID = book.id
    books = []
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        cur.execute("SELECT fk_Book from Favorites WHERE fk_User = ?", (userID,))
        result = cur.fetchall()
        for e in result:
            books.append(e["fk_Book"])
        works = True
    except Exception as e:
        msg = e
    return (works, msg, books)