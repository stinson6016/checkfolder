from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, DateField, SelectField
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    date_start = DateField(validators=[DataRequired()])
    date_end = DateField(validators=[DataRequired()])
    time_start = TimeField(validators=[DataRequired()])
    time_end = TimeField(validators=[DataRequired()])
    search = StringField("Search For?", validators=[Length(max=300)])
    computer = SelectField("Computer Name", validators=[Length(max=20)])
    submit = SubmitField("Search")
