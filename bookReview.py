from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets import TextArea 

class bookReviewForm(FlaskForm):
    score = IntegerField("Score", validators=[NumberRange(min = 0, max = 10, message="Notas de 0 a 10"), DataRequired()])
    review = TextAreaField("Review", validators=[DataRequired()])
    submit = SubmitField("Submit")