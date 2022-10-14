
# from flask import request
import sqlite3
import re
def db_register(request):
    msg = ""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Set variables
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Db Connect
        conn = sqlite3.connect("database/database.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

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
            cur.execute('INSERT INTO User VALUES (NULL, ?, ?, ?)', (username, password, email,))
            conn.commit()
            msg = 'Registrado com sucesso!'
    elif request.method == 'POST':
        msg = 'Preencha o formulario!'
    return msg