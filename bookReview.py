from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets import TextArea 

class bookReviewForm(FlaskForm):
    score = IntegerField("Score", validators=[NumberRange(min = 0, max = 10, message="From 0 to 10")])
    review = StringField("Review", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit")