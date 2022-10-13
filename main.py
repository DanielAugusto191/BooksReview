from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
import sqlite3
import urllib.request, json
import os
import re
from login_system import loginPage_BP
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

@app.route('/home')
def home():
    if 'loggedin' in session:
        # Get Books
        titulo = "O Ardiloso Cortes".replace(" ", "%20")
        url = "https://www.googleapis.com/books/v1/volumes?q=\"{}\"&orderBy=relevance&key=AIzaSyA6Z7tIcH7mawIpXKKUVrkVMNe4hD-uZNs".format(titulo)
        f = open("limao.txt", "a")
        response = urllib.request.urlopen(url)
        data = response.read()
        data = json.loads(data)
        bookList = []
        for i in range(len(data["items"])):  
            if "imageLinks" in data["items"][i]["volumeInfo"]:
                bookList.append([data["items"][i]["volumeInfo"]["title"], data["items"][i]["volumeInfo"]["imageLinks"]["smallThumbnail"]])
        f.close()
        return render_template('home.html', username=session['username'], titles=bookList)
    return redirect(url_for('loginPage.login'))

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        conn = sqlite3.connect("database/database.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('SELECT * FROM accounts WHERE id = ?', (session['id'],))
        account = cur.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('loginPage.login'))

