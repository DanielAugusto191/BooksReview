from flask import Blueprint, render_template, request, session, redirect, url_for
from database.db_login import db_register
loginPage_BP = Blueprint("loginPage", __name__, template_folder="templates")

@loginPage_BP.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("database/database.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        account = cur.execute('SELECT * FROM accounts WHERE username = ? AND password = ?', (username, password,)).fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('home'))
        else:
            msg = "Usuario ou senha errados!"
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
    msg = db_register(request)
    return render_template('register.html', msg=msg)