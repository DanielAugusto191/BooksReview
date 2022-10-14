from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
import sqlite3
import urllib.request, json
import os
import re
from login_system import loginPage_BP
from database.db_system import userInfo

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
    if 'loggedin' in session: # Aqui ta um exemplo de um request, é apenas um teste tem que mudar praticamente tudo, o primeiro passo provavel, é ver bem como dar o request e quais informações vao pegar, depois montar um digrama de classes de como vao quardar essas infos, tipo, classe Book, atributo titulo, capa, descrição. Metodo: getTitle() etc. 
        # Get Books
        titulo = "O Ardiloso Cortes".replace(" ", "%20")
        url = "https://www.googleapis.com/books/v1/volumes?q=\"{}\"&orderBy=relevance&key=AIzaSyA6Z7tIcH7mawIpXKKUVrkVMNe4hD-uZNs".format(titulo)
        response = urllib.request.urlopen(url)
        data = response.read()
        data = json.loads(data)
        bookList = []
        for i in range(len(data["items"])):  
            if "imageLinks" in data["items"][i]["volumeInfo"]:
                bookList.append([data["items"][i]["volumeInfo"]["title"], data["items"][i]["volumeInfo"]["imageLinks"]["smallThumbnail"]])
        return render_template('home.html', username=session['username'], titles=bookList)
    return redirect(url_for('loginPage.login'))

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        (works, msg, account) = userInfo(session["id"])
        return render_template('profile.html', account=account)
    return redirect(url_for('loginPage.login'))
