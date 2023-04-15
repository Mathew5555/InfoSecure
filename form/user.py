from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerField, BooleanField, \
    SelectMultipleField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')