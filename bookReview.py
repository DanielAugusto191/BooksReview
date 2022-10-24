from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, NumberRange, Optional
from wtforms.widgets import TextArea 

class bookReviewForm(FlaskForm):
    ch = [(None, ""), (1, 'Quero Ler'), (2, "Lendo"), (3, "Complete")]
    score = IntegerField("Score", validators=[NumberRange(min = 0, max = 10, message="Notas de 0 a 10"), Optional()])
    review = TextAreaField("Review", validators=[DataRequired()])
    status = SelectField("Status", choices=ch, validators=[Optional()])
    submit = SubmitField("Submit")