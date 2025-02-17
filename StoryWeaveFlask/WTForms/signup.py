from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import Email, DataRequired, InputRequired, Length


class SignupForm(FlaskForm):
    name = StringField("NAME :", validators=[DataRequired(), Length(min=1, max=50)], filters=[lambda x: x.strip() if x else x])
    emailID = EmailField("EMAIL ID :", validators=[DataRequired(), Email()])
    password = PasswordField("PASSWORD :", validators=[InputRequired()])
    submit = SubmitField("SUBMIT")
