from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
import sqlite3
import os
import re
from login_system import loginPage_BP
from database.db_system import userInfo
from bookSearch import bookSearch, SearchForm

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

@app.route('/home', methods=["POST", "GET"])
def home():
    if 'loggedin' in session:
        form = SearchForm()
        if form.validate_on_submit():
            data = bookSearch((form.searched.data).replace(" ", "%20"))
            form.searched.data = ''
        else:
            data = bookSearch("Skulduggery pleasant".replace(" ", "%20"))
        bookList = []
        if "items" in data:
            for i in range(len(data["items"])):  
                if "imageLinks" in data["items"][i]["volumeInfo"]:
                    bookList.append([data["items"][i]["volumeInfo"]["title"], data["items"][i]["volumeInfo"]["imageLinks"]["smallThumbnail"]])
        return render_template('home.html', form=form, username=session['username'], titles=bookList)
    return redirect(url_for('loginPage.login'))

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        (works, msg, account) = userInfo(session["id"])
        return render_template('profile.html', account=account)
    return redirect(url_for('loginPage.login'))
