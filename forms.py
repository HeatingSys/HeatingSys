from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators, SelectField, TextAreaField, RadioField, TimeField
from wtforms.widgets import TextArea
from wtforms.validators import InputRequired, EqualTo
from wtforms.fields.html5 import DateField
from datetime import datetime

class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=5, max=25)])
    password = PasswordField("Password", validators=[InputRequired()])
    password2 = PasswordField("Confirm password", validators=[InputRequired("Password doesn't match"), EqualTo("password")])
    email = StringField("Email Address", [validators.Length(min=6, max=100)])
    accept_rules = BooleanField("I accept the terms and conditions", validators=[InputRequired()])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired("Username doesn't exist")])
    password = PasswordField("Password", validators=[InputRequired()])
    password2 = PasswordField("Confirm password", validators=[InputRequired("Password doesn't match"), EqualTo("password")])
    submit = SubmitField("Login")

class RoomForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    automation = BooleanField("Energy automation tool", validators=[InputRequired()])
    submit = SubmitField("Save")

class ScheduleForm(FlaskForm):
    desiredTemp = StringField('Enter the desired temperature: ', validators=[InputRequired()])
    startTime = StringField("Start at", validators=[InputRequired()])
    endTime = StringField("End at", validators=[InputRequired()])
    submit = SubmitField("Save")