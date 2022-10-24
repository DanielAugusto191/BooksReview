from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from database.db_system import updateUsername, updateBiografy, updatePassword
import re
import os
from database.db_system import userInfo, getAllReviews, getRate, getBookByID, updateProfilePicture, getBookRateByID
from werkzeug.utils import secure_filename
import uuid as uuid

profilePage_BP = Blueprint("profilePage", __name__, template_folder="templates")

class profileForm(FlaskForm):
    username = StringField("Nome")
    oldPassword = PasswordField("Antiga senha")
    password = PasswordField("Senha")
    bio = TextAreaField("Biografia")
    profile_pic = FileField("Foto de Perfil")
    submit = SubmitField("Enviar")

@profilePage_BP.route('/profile')
def profile():
    if 'loggedin' in session:
        (works, msg, account) = userInfo(session["id"])
        bookList = []
        (works, msg, result) = getAllReviews(session["id"])
        for e in result:
            (_,_,book) = getBookByID(e["fk_Book"])
            (works, msg, resultRate) = getRate(session["id"], book)
            if not works:
                resultresultRate = "Voce nao avaliou esse livro!"
            (_, _, bookRate) = getBookRateByID(book.id)
            bookList.append({"book": book, "review": e["review"], "rate": resultRate, "bookRate": bookRate})
        return render_template('profile.html', account=account, username=session['username'], books=bookList)
    return redirect(url_for('loginPage.login'))

@profilePage_BP.route('/profile_edit', methods=['GET', 'POST'])
def profileEdit():
    
    if 'loggedin' in session:
        (works, msg, account) = userInfo(session["id"])
        profForm = profileForm()
        if hasattr(account, 'keys') and 'bio' in account.keys():
            profForm.bio.data = account['bio']
        if profForm.validate_on_submit():
            if profForm.username.data != "":
                (works, msg) = updateUsername(session['id'], profForm.username.data)
                profForm.username.data = ""
            if profForm.oldPassword.data != "" and profForm.password.data != "":
                (works, msg) = updatePassword(session['id'], profForm.oldPassword.data, profForm.password.data)
            if profForm.bio.data != "":
                (works, msg) = updateBiografy(session['id'], profForm.bio.data)
                profForm.bio.data = ""
            if profForm.profile_pic.data.filename != "":
                picFilename = secure_filename(profForm.profile_pic.data.filename)
                picName = str(uuid.uuid1()) + "_" + picFilename
                profForm.profile_pic.data.save(os.path.join("static/profilePics/", picName))
                (works, msg) = updateProfilePicture(session['id'], picName)
        #return redirect(url_for('profilePage.profile'))
        return render_template("profile_edit.html", form = profForm)
    return redirect(url_for('loginPage.login')) 