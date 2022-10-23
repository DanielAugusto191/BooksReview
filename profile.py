from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
import re
from database.db_system import userInfo

profilePage_BP = Blueprint("profilePage", __name__, template_folder="templates")

class profileForm(FlaskForm):
    username = StringField("Nome")
    oldPassword = StringField("Antiga senha")
    password = PasswordField("Senha")
    email = StringField("Email")
    bio = TextAreaField("Biografia")
    profile_pic = FileField("Foto de Perfil")
    submit = SubmitField("Enviar")

@profilePage_BP.route('/profile')
def profile():
    if 'loggedin' in session:
        (works, msg, account) = userInfo(session["id"])
        return render_template('profile.html', account=account, username=session['username'])
    return redirect(url_for('loginPage.login'))

@profilePage_BP.route('/profile_edit')
def profileEdit():
    if 'loggedin' in session:
        return render_template("profile_edit.html")
    return redirect(url_for('loginPage.login')) 