from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators, SelectField, TextAreaField, RadioField, TimeField
from wtforms.widgets import TextArea
from wtforms.validators import InputRequired, EqualTo
from wtforms.fields.html5 import DateField
from datetime import datetime

class RoomForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    automation = BooleanField("Energy automation tool", default=True, validators=[InputRequired()])
    submit = SubmitField("Save")

class ScheduleForm(FlaskForm):
    desiredTemp = StringField('Enter the desired temperature: ', validators=[InputRequired()])
    startTime = StringField("Start at", validators=[InputRequired()])
    endTime = StringField("End at", validators=[InputRequired()])
    submit = SubmitField("Save")