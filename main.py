import os

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import Boolean, Integer, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from forms import CafeForm


class Base(DeclarativeBase):
    pass


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, instance_path=os.path.join(BASE_DIR, "instance"))
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"

db = SQLAlchemy(model_class=Base)
db.init_app(app)
csrf = CSRFProtect(app)


class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=True)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


def format_price(value):
    return f"£{float(value):.2f}"


@app.route("/")
def home():
    selected = request.args.get("location", "")
    query = select(Cafe).order_by(Cafe.name)
    if selected:
        query = query.where(Cafe.location == selected)
    cafes = db.session.execute(query).scalars().all()
    locations = db.session.execute(
        select(Cafe.location).distinct().order_by(Cafe.location)
    ).scalars().all()
    return render_template("index.html", cafes=cafes, locations=locations, selected=selected)


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        name = form.name.data.strip()
        exists = db.session.execute(select(Cafe).where(Cafe.name == name)).scalar()
        if exists:
            form.name.errors.append("A cafe with this name already exists.")
        else:
            new_cafe = Cafe(
                name=name,
                map_url=form.map_url.data,
                img_url=form.img_url.data,
                location=form.location.data.strip(),
                seats=form.seats.data,
                has_toilet=form.has_toilet.data,
                has_wifi=form.has_wifi.data,
                has_sockets=form.has_sockets.data,
                can_take_calls=form.can_take_calls.data,
                coffee_price=format_price(form.coffee_price.data),
            )
            db.session.add(new_cafe)
            db.session.commit()
            flash(f"{new_cafe.name} was added.", "success")
            return redirect(url_for("home"))
    return render_template("add.html", form=form)


@app.route("/update-price/<int:cafe_id>", methods=["POST"])
def update_price(cafe_id):
    cafe = db.get_or_404(Cafe, cafe_id)
    try:
        new_price = float(request.form.get("coffee_price", ""))
    except ValueError:
        flash("Please enter a valid price.", "danger")
    else:
        if new_price < 0:
            flash("The price cannot be negative.", "danger")
        else:
            cafe.coffee_price = format_price(new_price)
            db.session.commit()
            flash(f"Coffee price for {cafe.name} updated to {cafe.coffee_price}.", "success")
    return redirect(url_for("home", location=request.args.get("location") or None))


@app.route("/delete/<int:cafe_id>", methods=["POST"])
def delete_cafe(cafe_id):
    cafe = db.get_or_404(Cafe, cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    flash(f"{cafe.name} was deleted.", "warning")
    return redirect(url_for("home", location=request.args.get("location") or None))


if __name__ == "__main__":
    app.run(debug=True)
