from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SubmitField, validators, SelectField, TextAreaField, RadioField, TimeField
from wtforms.widgets import TextArea
from wtforms.validators import InputRequired, EqualTo, NumberRange
from wtforms.fields.html5 import DateField
from datetime import datetime

class RoomForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    submit = SubmitField("Save")

class ScheduleForm(FlaskForm):
    desiredTemp = StringField('Enter the desired temperature: ', validators=[InputRequired()])
    startTime = StringField("Start at", validators=[InputRequired()])
    endTime = StringField("End at", validators=[InputRequired()])
    submit = SubmitField("Save")

class SettingForm(FlaskForm):
    heatingAppliancePower = IntegerField('Enter the power of your heating appliance (in watts)', validators=[InputRequired(), NumberRange(min=500, max=2000, message='- Input must be between 500 and 2000')])
    energyLimit = IntegerField('Enter the monthly energy limit you do not want to exceed (in kilo-watt hour)', validators=[InputRequired(), NumberRange(min=0, max=350, message='- Input must be between 0 and 350')])
    submit = SubmitField("Submit")