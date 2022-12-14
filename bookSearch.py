from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

import urllib.request, json

class SearchForm(FlaskForm):
    searched = StringField("Searched")
    sortBy = SelectField('Sort by', choices = [('relevance', 'Relevance'), ('title', 'Title'), ('authors', 'Authors')])
    submit = SubmitField("Submit")

def bookSearch(bookName):
    url = "https://www.googleapis.com/books/v1/volumes?q=\"{}\"Type=books&orderBy=relevance&key=AIzaSyCuHdDuHmXyIuvAHZgdc94kl-W5Tek3lco".format(bookName)
    response = urllib.request.urlopen(url)
    data = response.read()
    data = json.loads(data)
    return data