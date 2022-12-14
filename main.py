import string
from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
import sqlite3
import os
import re

from loginSystem import loginPage_BP
from profile import profilePage_BP
from database.db_system import userInfo, getAllStatus, getBookByID, setRate, setReview, getReview, setStatus
from bookSearch import bookSearch, SearchForm
from Book import Book, sortBookList
from bookReview import bookReviewForm

app = Flask(__name__)
app.secret_key = "LIMAO"
app.config['ENVIRONMENT_VAR'] = 'FLASK_APP'
app.config["SQL_HOST"] = "localhost"
app.config['SQL_USER'] = 'root'
app.config['SQL_DB'] = 'database'
app.register_blueprint(loginPage_BP)
app.register_blueprint(profilePage_BP)

def main():
    app.run(host='127.0.0.1', port=5000)

if __name__ == "__main__":
    main()

searched = "Skulduggery pleasant".replace(" ", "%20")

@app.route('/home', methods=["POST", "GET"])
def home():
    if 'loggedin' in session:
        searchForm = SearchForm()
        global searched
        bookList = []
        if searchForm.validate_on_submit():
            if searchForm.searched.data != None:
                searched = (searchForm.searched.data).replace(" ", "%20")
            data = bookSearch(searched)
            if "items" in data:
                for i in range(len(data["items"])):  
                    if (("imageLinks" in data["items"][i]["volumeInfo"]) and ("description" in data["items"][i]["volumeInfo"])
                    and ("authors" in data["items"][i]["volumeInfo"])):
                        bookList.append(Book(data["items"][i]))
                if(searchForm.sortBy.data is not None):
                    bookList = sortBookList(bookList, searchForm.sortBy.data)
        return render_template('home.html', searchForm = searchForm, username=session['username'], titles=bookList)
    return redirect(url_for('loginPage.login'))

@app.route('/addReview', methods=["GET", "POST"])
def addReview():
    if 'loggedin' in session:
        reviewForm = bookReviewForm()
        (works, msg, account) = userInfo(session["id"])
        if request.method == "GET":
            title = request.args.get('title', None)
            authors = request.args.get('authors', None)
            imageLink = request.args.get('imageLink', None)
            description = request.args.get('description', None)
            bkid = request.args.get('bkid', None)
            bb = {"id": bkid, "volumeInfo": {"title": title, "authors": authors, "description": description, "imageLinks": {"smallThumbnail": imageLink}}}
            session["book"] = bb
            bb = Book(bb)
            (_,_,rr) = getReview(session["id"], bb)
            if hasattr(rr, 'keys') and 'review' in rr.keys():
                reviewForm.review.data = rr['review']
        if reviewForm.validate_on_submit():
            book = Book(session['book'])
            ch = [(None, ""), (1, 'Quero Ler'), (2, "Lendo"), (3, "Complete")]
            if reviewForm.score.data != None:
                setRate(session['id'], book, reviewForm.score.data)
            if reviewForm.review.data != "":
                setReview(session['id'], book, reviewForm.review.data)
            if reviewForm.status.data != "None":
                setStatus(session['id'], book, int(reviewForm.status.data))
            reviewForm.review = ''
            return redirect(url_for('profilePage.profile'))
        return render_template('addReview.html', reviewForm = reviewForm, account=account, username=session['username'], book=bb)
    return redirect(url_for('loginPage.login'))

@app.route('/wantRead')
def wantRead():
    if 'loggedin' in session:
        (works, msg, status) = getAllStatus(session['id'])
        bookList = []
        if works:
            for e in status:
                if e['status'] == 1:
                    bookList.append({'date': e['date'], 'book': getBookByID(e['fk_Book'])[2]})
        return render_template("wantRead.html", books = bookList)
    return redirect(url_for('loginPage.login')) 

@app.route('/reading')
def reading():
    if 'loggedin' in session:
        (works, msg, status) = getAllStatus(session['id'])
        bookList = []
        if works:
            for e in status:
                if e['status'] == 2:
                    bookList.append({'date': e['date'], 'book': getBookByID(e['fk_Book'])[2]})
        return render_template("reading.html", books = bookList)
    return redirect(url_for('loginPage.login'))

@app.route('/readed')
def readed():
    if 'loggedin' in session:
        (works, msg, status) = getAllStatus(session['id'])
        bookList = []
        if works:
            for e in status:
                if e['status'] == 3:
                    bookList.append({'date': e['date'], 'book': getBookByID(e['fk_Book'])[2]})
        return render_template("readed.html", books = bookList)
    return redirect(url_for('loginPage.login'))