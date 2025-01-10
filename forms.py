from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, EqualTo


class AddAlbumForm(FlaskForm):
    name = StringField("Album Name", validators=[DataRequired()])
    image = FileField("Album Image", validators=[
        DataRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Add Album')


class AddAlbumSongForm(FlaskForm):
    name = StringField('name')


class AddSingleForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    image = FileField("File", validators=[DataRequired()])
    submit = SubmitField('Add')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=3, max=20)])
    repeat_password = PasswordField("Repeat Password",
                                    validators=[DataRequired(), EqualTo('password', message="not the same password")])
    submit = SubmitField("Register")


class AlbumRegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=3, max=20)])
    repeat_password = PasswordField("Repeat Password",
                                    validators=[DataRequired(), EqualTo('password', message="not the same password")])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=3, max=20)])
    submit = SubmitField("login")


class AlbumloginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=3, max=20)])
    submit = SubmitField("login")
