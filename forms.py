from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, IntegerField, SelectField, FileField,
from wtforms.validators import DataRequired, Length, EqualTo


class SignupForm(FlaskForm):
    username = StringField(
        "Username: ",
        validators=[
            DataRequired(),
            Length(
                6,
                32,
                message="Username lenght must be from 6 to 32 symbols",
            ),
        ],
    )
    password = PasswordField(
        "Password: ",
        validators=[
            DataRequired(),
            Length(8, 32, message="Password lenght must be from 8 to 32 symbols"),
        ],
    )
    password_rep = PasswordField("Repeat password: ", validators=[EqualTo("password")])


class SigninForm(FlaskForm):
    username = StringField(
        "Username: ",
        validators=[
            DataRequired(),
            Length(
                6,
                32,
                message="Username lenght must be from 6 to 32 symbols",
            ),
        ],
    )
    password = PasswordField(
        "Password: ",
        validators=[
            DataRequired(),
            Length(8, 32, message="Password lenght must be from 8 to 32 symbols"),
        ],
    )

class FileForm(FlaskForm):
    file = FileField(
        'File',
        validators=[DataRequired(),
        ],
    )
    expiring_choice = SelectField(
        "Expiring: ",
        choices=[
            (60*60*24*7, '7 days'),
            (60*60*24*14, "14 days"),
            ('one_time', "1 downloading(will be deleted after only 1 downloading)"),
        ],
        validators=[DataRequired()],
    )

class WYWTDForm(FlaskForm):
    task = SelectField(
        'What do you want to do?: ',
        choices=[
            ('download', 'download'),
            ('upload', 'upload'),
        ],
    )

class DownloadForm(FlaskForm):
    link = StringField(
        'File link code: ',
        validators=[
            DataRequired(),
            Length(8,8, message='link has to be 8-letters code ')

        ],
    )