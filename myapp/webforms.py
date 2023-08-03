from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, DateField, SelectField, EmailField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    date_start = DateField(validators=[DataRequired()])
    date_end = DateField(validators=[DataRequired()])
    time_start = TimeField(validators=[DataRequired()])
    time_end = TimeField(validators=[DataRequired()])
    search = StringField("Search For?")
    computer = SelectField("Computer Name")
    submit = SubmitField("Search")
