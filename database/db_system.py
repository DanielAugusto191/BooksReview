# Aqui vai ter request ao banco para profiles.
import sqlite3
import datetime
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
        conn = sqlite3.connect("database/database.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('SELECT * FROM User WHERE id = ?', (id,))
        account = dict(cur.fetchone())
        del account["password"]
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
        conn = sqlite3.connect("database/database.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('SELECT password FROM User WHERE id = ?', (id,))
        result = dict(cur.fetchone())
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
        conn = sqlite3.connect("database/database.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("UPDATE User SET username = ? WHERE id = ?", (newUserName, id,))
        conn.commit()
        works = True
        msg = "Update com sucesso!"
    except Exception as e:
        msg = e
    return (works, msg)

def setReview(userID, bookID, review):
    ''' 
Set a new review of a book

Parameters:
userID = User id
bookID = Book id
Review = String with the user review.

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = ""/"{error}" - Status of works.
'''
    works = False
    msg = ""
    try:
        conn = sqlite3.connect("database/database.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("INSERT INTO Review (fk_User, fk_Book, review, date) VALUES (?, ?, ?, ?)", (userID, bookID,  review, datetime.datetime.now()))
        conn.commit()
        works = True
        msg = "Review adicionado!"
    except Exception as e:
        msg = e
    return (works, msg)

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
    pass

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
    review = Users review (that are Dicts of Books ID, Books name, rate and Review) - {"BookID"=ID, "BookName"=BooksName, "rate"=rate, "review"=Review}
'''
    pass

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
    pass

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
'''
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
    pass

def getRate():
    pass

def getAllRate():
    pass

def toogleBookAsFavorite(UserID, bookID):
    ''' 
Set/Unset a book as users favorite. (Limit of 5 books)

Parameters:
userID = User id
bookID = Book id

Return:
Tuple of:
    works = True/False - If there is no error.
    msg = ""/"{error}" - Status of works.
'''
    pass

def requestFavoritesBooks(UserID, bookID):
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
    pass