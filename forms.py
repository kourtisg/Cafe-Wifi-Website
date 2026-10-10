"""Forms for the cafe and wifi application."""

try:
    from flask_wtf import FlaskForm  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover - fallback for environments without Flask-WTF
    class FlaskForm:  # type: ignore[no-redef]
        """Fallback FlaskForm stub used when Flask-WTF is unavailable."""

        pass

from wtforms import BooleanField, DecimalField, SelectField, StringField, SubmitField
from wtforms.validators import URL, DataRequired, InputRequired, Length, NumberRange

SEAT_CHOICES = ["0-10", "10-20", "20-30", "30-40", "40-50", "50+"]


class CafeForm(FlaskForm):
    name = StringField("Cafe name", validators=[DataRequired(), Length(max=250)])
    location = StringField("Location", validators=[DataRequired(), Length(max=250)])
    map_url = StringField("Google Maps URL", validators=[DataRequired(), URL(), Length(max=500)])
    img_url = StringField("Image URL", validators=[DataRequired(), URL(), Length(max=500)])
    seats = SelectField("Seats", choices=SEAT_CHOICES)
    coffee_price = DecimalField(
        "Coffee price (£)", places=2, validators=[InputRequired(), NumberRange(min=0)]
    )
    has_wifi = BooleanField("Wifi")
    has_sockets = BooleanField("Power sockets")
    has_toilet = BooleanField("Toilet")
    can_take_calls = BooleanField("OK to take calls")
    submit = SubmitField("Add cafe")
