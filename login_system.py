import sqlite3
from flask import Blueprint, render_template, request, session, redirect, url_for
from database.db_login import db_register
from database.db_login import db_login
loginPage_BP = Blueprint("loginPage", __name__, template_folder="templates")

@loginPage_BP.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    (result, msg, account) = db_login(request)
    if result:
        session['loggedin'] = True
        session['id'] = account['id']
        session['username'] = account['username']
        return render_template('home.html', msg=msg, username=session["username"])
    return render_template('index.html', msg=msg)

@loginPage_BP.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('loginPage.login'))

@loginPage_BP.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    (result, msg) = db_register(request)[1]
    return render_template('register.html', msg=msg)