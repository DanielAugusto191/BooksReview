
import sqlite3
import re
def db_register(request):
    works = False
    msg = ""
    print(request.form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Set variables
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Db Connect
        conn = sqlite3.connect("database/database.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        #Query
        cur.execute('SELECT * FROM User WHERE username = ?', (username,))
        account = cur.fetchone()
        if account:
            msg = 'Essa conta já existe!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Email invalido!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Nome deve apenas conter letras e números!'
        elif not username or not password or not email:
            msg = 'Preencha o formulario completo!'
        else:
            cur.execute('INSERT INTO User VALUES (NULL, ?, ?, ?, ?, ?)', (username, password, email,None,None))
            conn.commit()
            msg = 'Registrado com sucesso!'
            works = True
    elif request.method == 'POST':
        msg = 'Preencha o formulario!'
    return (works, msg)

def db_login(request):
    msg = ""
    works = False
    account = ""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Set variables
        username = request.form['username']
        password = request.form['password']

        # Conn
        conn = sqlite3.connect("database/database.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Query
        account = cur.execute('SELECT * FROM User WHERE username = ? AND password = ?', (username, password,)).fetchone()
        if account:
            works = True
        else:
            msg = "Usuario ou senha errados!"
            works = False
    return (works, msg, account)