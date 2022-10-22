# Aqui vai ter request ao banco para profiles.
# from sys import path
# path.insert(0, "/home/pc2/facul/sem8/ES/BooksReview/")

import datetime
from database.db_checks import *
from database.db_connect import *
from Book import Book
"""
Summary:

userInfo(id) - Given a user id return yours info.
updatePassword(id, oldPassword, newPassword) -  Update user's password
updateProfilePicture(id, newProfilePicture) - Update user's profile picture
updateUsername(id, newUserName) - Update user's username
setReview(userID, bookID, review) - Set a new review of a book
updateReview(userID, bookID, review) - Update a review of a book
getReview(userID, bookID) - Get a User's review of a book
getAllReviews(userID) - Get all reviews of a User
setRate(userID, bookID, rate) - Assigns the rate the user has given to a book
updateRate(userID, bookID, newRate) - Update the rate the user has given to a book
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
    works = False
    msg = ""
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
        print(bb)
        
        works = True
        msg = "ok"
    except Exception as e:
        msg = e
    return (works, msg)

### REVIEW ####

# TODO: bookID turns into Book Object
def setReview(userID, bookID, review):
    ''' 
Set a new review of a book

Parameters:
userID = User id
bookObject = Object with book's informations
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
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        if not checkBook(bookID):
            raise Exception("Invalid BookID!")

        # TODO: Check if book is on DB, if its not, look on API and add book.
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

# TODO: bookID turns into bookObject
def updateReview(userID, bookID, review):
    ''' 
Update a review of a book

Parameters:
userID = User id
bookID = Book id
Review = String with the new user review.

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = ""/"{error}" - Status of works.
'''
    works = False
    msg = ""
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        if not checkBook(bookID):
            raise Exception("Invalid BookID!")
        cur.execute("UPDATE Review SET review = ? WHERE fk_User = ? and fk_Book = ?", (review, userID, bookID,))
        conn.commit()
        works = True
    except Exception as e:
        msg = e
    return (works, msg)


def getReview(userID, bookID):
    ''' 
Get a User's review of a book

Parameters:
userID = User id
bookID = Book id

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = ""/"{error}" - Status of works.
    review = Users review (that are Dicts of Date and Review) - {"date"=2022-01-022 10:37:35.123456, "review"=Review}
'''
    works = False
    msg = ""
    review = ""
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        if not checkBook(bookID):
            raise Exception("Invalid BookID!")
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
def delReview(userID, bookID):
    works = False
    msg = ""
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        if not checkBook(bookID):
            raise Exception("Invalid BookID!")
        cur.execute("DELETE FROM review WHERE fk_User = ? and fk_Book = ?", (userID, bookID))
        conn.commit()
        works = True
        msg = ""
    except Exception as e:
        msg = e
    return (works, msg)

### RATE ####

def setRate(userID, bookID, rate):
    ''' 
Assigns the rate the user has given to a book

Parameters:
userID = User id
bookID = Book id
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
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        if not checkBook(bookID):
            raise Exception("Invalid BookID!")

        cur.execute('SELECT id, date FROM Rate WHERE fk_User = ? and fk_Book = ?', (userID, bookID))
        result = cur.fetchone()
        if result == None:
            cur.execute("INSERT INTO Rate (fk_User, fk_Book, rate, date) VALUES (?, ?, ?, ?)", (userID, bookID,  rate, datetime.datetime.now()))
            conn.commit()
            works = True
            msg = "Rate adicionado!"
        else:
            result = dict(result)
            if result:
                msg = ("Você ja fez uma nota para esse livro!" )
    except Exception as e:
        msg = e
    return (works, msg, result)
    pass

def updateRate(userID, bookID, newRate):
    ''' 
Update the rate the user has given to a book

Parameters:
userID = User id
bookID = Book id
newRate = The rate that user gives to the book.

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = ""/"{error}" - Status of works.
'''
    works = False
    msg = ""
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        if not checkBook(bookID):
            raise Exception("Invalid BookID!")
        cur.execute("UPDATE rate SET rate = ? WHERE fk_User = ? and fk_Book = ?", (newRate, userID, bookID,))
        conn.commit()
        works = True
    except Exception as e:
        msg = e
    return (works, msg)

def getRate(userID, bookID):
    works = False
    msg = ""
    result = None
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        if not checkBook(bookID):
            raise Exception("Invalid BookID!")
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

def delRate(userID, bookID):
    works = False
    msg = ""
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        if not checkBook(bookID):
            raise Exception("Invalid BookID!")
        cur.execute("DELETE FROM rate WHERE fk_User = ? and fk_Book = ?", (userID, bookID))
        conn.commit()
        works = True
        msg = ""
    except Exception as e:
        msg = e
    return (works, msg)

### STATUS ####
# 0 - Unreaded, 1 - Want to read, 2 - Reading, 3 - Complete

def setStatus(userID, bookID, status):
    works = False
    msg = ""
    try:
        (conn, cur) = connectDatabase()
        if checkStatus(status):
            raise Exception("Invalid Status")
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        if not checkBook(bookID):
            raise Exception("Invalid BookID!")
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

def getStatus(userID, bookID):
    works = False
    msg = ""
    result = None
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        if not checkBook(bookID):
            raise Exception("Invalid BookID!")
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

def delStatus(userID, bookID):
    works = False
    msg = ""
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        if not checkBook(bookID):
            raise Exception("Invalid BookID!")
        cur.execute("DELETE FROM status WHERE fk_User = ? and fk_Book = ?", (userID, bookID))
        conn.commit()
        works = True
        msg = ""
    except Exception as e:
        msg = e
    return (works, msg)

### FAVORITES ####
def toogleBookAsFavorite(userID, bookID):
    ''' 
Set/Unset a book as users favorite.

Parameters:
userID = User id
bookID = Book id

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = "on/off" / "{error}" - Status of works. on = addde, off = removed
'''
    works = False
    msg = ""
    try:
        (conn, cur) = connectDatabase()
        if not checkUser(userID):
            raise Exception("Invalid UserID!")
        if not checkBook(bookID):
            raise Exception("Invalid BookID!")
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
bookID = Book id

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = ""/"{error}" - Status of works.
    Books = List of Reviews(that are Dicts of Books ID, Books name, rate and Review) - [{"BookID"=ID, "BookName"=BooksName,"rate"=rate, "review"=Review}, {"BookID"=ID, "BookName"=BooksName, "rate"=rate, "review"=Review}, ...]
'''
    works = False
    msg = ""
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