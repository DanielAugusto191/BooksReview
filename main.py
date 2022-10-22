import string
from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
import sqlite3
import os
import re

from login_system import loginPage_BP
from database.db_system import userInfo
from bookSearch import bookSearch, SearchForm
from Book import Book, sortBookList

app = Flask(__name__)
app.secret_key = "LIMAO"
app.config['ENVIRONMENT_VAR'] = 'FLASK_APP'
app.config["SQL_HOST"] = "localhost"
app.config['SQL_USER'] = 'root'
app.config['SQL_PASSWORD'] = '123'
app.config['SQL_DB'] = 'BooksReview'
app.register_blueprint(loginPage_BP)

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
        if searchForm.validate_on_submit():
            if searchForm.searched.data != None:
                searched = (searchForm.searched.data).replace(" ", "%20")
        data = bookSearch(searched)
        bookList = []
        if "items" in data:
            for i in range(len(data["items"])):  
                if (("imageLinks" in data["items"][i]["volumeInfo"]) and ("description" in data["items"][i]["volumeInfo"])
                and ("authors" in data["items"][i]["volumeInfo"])):
                    bookList.append(Book(data["items"][i]))
        if(searchForm.sortBy.data is not None):
            bookList = sortBookList(bookList, searchForm.sortBy.data)
        return render_template('home.html', searchForm = searchForm, username=session['username'], titles=bookList)
        #return render_template('home.html', searchForm = searchForm, sortForm = sortForm, username=sortForm.sortBy.data, titles=bookList)
    return redirect(url_for('loginPage.login'))

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        (works, msg, account) = userInfo(session["id"])
        return render_template('profile.html', account=account, username=session['username'])
    return redirect(url_for('loginPage.login'))
