from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField,\
    BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, \
    EqualTo, Email, ValidationError

from src.models import User, Task


class TaskForm(FlaskForm):
    """Form for adding new car"""
    description = StringField('Zadanie', validators=[DataRequired()])
    # date_due
    def validate(self) -> bool:
        """Additional validation goes here"""
        if not FlaskForm.validate(self):
            return False
        return True


class LoginForm(FlaskForm):
    """Login form"""
    name = StringField('Użytkownik', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember_me = BooleanField('Pozostań zalogowany')
    submit = SubmitField('Zaloguj')


class SignInForm(FlaskForm):
    name = StringField(
        'Użytkownik', validators=[
            DataRequired(), Length(3, 80),
            Regexp('^[A-Za-z0-9_]{3,}$',
                   message='Dopuszczalne litery, cyfry oraz podkreślenia')
        ]
    )
    email = StringField('Email', validators=[DataRequired(), Length(1, 120),
                                             Email()])
    password = PasswordField(
        'Hasło', validators=[
            DataRequired(),
            EqualTo('password2', message='Hasła muszą być identyczne')
        ]
    )
    password2 = PasswordField('Potwierdź hasło', validators=[DataRequired()])

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('Adres email jest już zajęty')

    def validate_user(self, user_field):
        if User.query.filter_by(email=user_field.data).first():
            raise ValidationError('Nazwa użytkownika jest już zajęta')
