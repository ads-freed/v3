from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class TicketForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=140)])
    description = TextAreaField('Description', validators=[DataRequired()])
    attachment = FileField('Attachment')
    submit = SubmitField('Create Ticket')

class TicketReplyForm(FlaskForm):
    content = TextAreaField('Reply', validators=[DataRequired()])
    attachment = FileField('Attachment')
    submit = SubmitField('Submit Reply')

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password')
    submit = SubmitField('Update Profile')

class MessageForm(FlaskForm):
    content = TextAreaField('Message', validators=[DataRequired()])
    attachment = FileField('Attachment')
    submit = SubmitField('Send Message')
