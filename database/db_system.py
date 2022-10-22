# Aqui vai ter request ao banco para profiles.
import datetime
import db_checks
import db_connect
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
        (conn, cur) = db_connect.connectDatabase()
        if not db_checks.checkUser(id):
            raise Exception("Invalid UserID!")
        cur.execute('SELECT * FROM User WHERE id = ?', (id,))
        account = cur.fetchone()
        if account == None:
            raise Exception("ID invalido!")
        account = dict(account)
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
        (conn, cur) = db_connect.connectDatabase()
        if not db_checks.checkUser(id):
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
        (conn, cur) = db_connect.connectDatabase()
        if not db_checks.checkUser(id):
            raise Exception("Invalid UserID!")
        cur.execute("UPDATE User SET username = ? WHERE id = ?", (newUserName, id,))
        conn.commit()
        works = True
        msg = "Update com sucesso!"
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
        (conn, cur) = db_connect.connectDatabase()
        if not db_checks.checkUser(userID):
            raise Exception("Invalid UserID!")
        if not db_checks.checkBook(bookID):
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
        (conn, cur) = db_connect.connectDatabase()
        if not db_checks.checkUser(userID):
            raise Exception("Invalid UserID!")
        if not db_checks.checkBook(bookID):
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
        (conn, cur) = db_connect.connectDatabase()
        if not db_checks.checkUser(userID):
            raise Exception("Invalid UserID!")
        if not db_checks.checkBook(bookID):
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
        (conn, cur) = db_connect.connectDatabase()
        if not db_checks.checkUser(userID):
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
        (conn, cur) = db_connect.connectDatabase()
        if not db_checks.checkUser(userID):
            raise Exception("Invalid UserID!")
        if not db_checks.checkBook(bookID):
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
        (conn, cur) = db_connect.connectDatabase()
        if not db_checks.checkUser(userID):
            raise Exception("Invalid UserID!")
        if not db_checks.checkBook(bookID):
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
        (conn, cur) = db_connect.connectDatabase()
        if not db_checks.checkUser(userID):
            raise Exception("Invalid UserID!")
        if not db_checks.checkBook(bookID):
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
        (conn, cur) = db_connect.connectDatabase()
        if not db_checks.checkUser(userID):
            raise Exception("Invalid UserID!")
        if not db_checks.checkBook(bookID):
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
        (conn, cur) = db_connect.connectDatabase()
        if not db_checks.checkUser(userID):
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
        (conn, cur) = db_connect.connectDatabase()
        if not db_checks.checkUser(userID):
            raise Exception("Invalid UserID!")
        if not db_checks.checkBook(bookID):
            raise Exception("Invalid BookID!")
        cur.execute("DELETE FROM rate WHERE fk_User = ? and fk_Book = ?", (userID, bookID))
        conn.commit()
        works = True
        msg = ""
    except Exception as e:
        msg = e
    return (works, msg)

### STATUS ####
def setStatus():
    pass

def getStatus():
    pass

def getAllStatus():
    pass

def delStatus():
    pass

### FAVORITES ####
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