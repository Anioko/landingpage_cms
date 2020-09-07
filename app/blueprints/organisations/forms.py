from app.models import *
from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import Length, Required, ValidationError, InputRequired, Email, Optional

images = UploadSet('images', IMAGES)


class LogoForm(FlaskForm):
    logo = FileField('Logo', validators=[FileRequired(), FileAllowed(images, 'Images only!')])
    submit = SubmitField('Submit')

    
class InviteUserForm(FlaskForm):
    first_name = StringField(
        'First name', validators=[InputRequired(),
                                  Length(1, 64)])
    last_name = StringField(
        'Last name', validators=[InputRequired(),
                                 Length(1, 64)])
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    submit = SubmitField('Invite')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
