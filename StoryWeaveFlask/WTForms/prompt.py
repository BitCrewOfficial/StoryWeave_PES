from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, RadioField
from wtforms.validators import DataRequired


class PromptForm(FlaskForm):
    prompt = TextAreaField("Enter your prompt :", validators=[DataRequired()])
    language = RadioField(
        "Select in which language you need to generate :",
        choices=[
            ("eng", "ENGLISH"),
            ("spa", "SPAINISH"),
            ("fre", "FRENCH"),
            ("hin", "HINDI"),
            ("kan", "KANNADA"),
            ("tam", "TAMIL"),
            ("tel", "TELUGU"),
            ("mal", "MALAYALAM"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("SUMBIT")


class HistoryButton(FlaskForm):
    history = SubmitField("View Past Prompts")


class BackButton(FlaskForm):
    back = SubmitField("Go Back To Prompt")
