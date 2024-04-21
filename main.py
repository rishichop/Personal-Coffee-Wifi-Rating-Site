from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, TimeField, RadioField
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafe.db"

db.init_app(app)


class cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cafe_name: Mapped[str] = mapped_column(String(250), nullable=False)
    location_url: Mapped[str] = mapped_column(String(250), nullable=False)
    open_time: Mapped[str] = mapped_column(String(10), nullable=False)
    close_time: Mapped[str] = mapped_column(String(10), nullable=False)
    coffee_rating: Mapped[str] = mapped_column(String(50), nullable=False)
    wifi_rating: Mapped[str] = mapped_column(String(50), nullable=False)
    power_rating: Mapped[str] = mapped_column(String(50), nullable=False)


# with app.app_context():
#     db.create_all()
#     db.session.add(cafe(
#         cafe_name="Rishi cafe",
#         location_url="Somewhere",
#         open_time="12:00",
#         close_time="12:00",
#         coffee_rating="☕☕☕",
#         wifi_rating="💪💪💪💪💪",
#         power_rating="🔌🔌"
#         ))
#     db.session.commit()


class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name',
                       validators=[DataRequired()])

    location_url = URLField(label='Location',
                            validators=[DataRequired()])

    open = TimeField(label='Open Time',
                     validators=[DataRequired()])

    close = TimeField(label='Close Time',
                      validators=[DataRequired()])

    coffee_rate = RadioField(label="Coffee Rating",
                             validators=[DataRequired()],
                             choices=["☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"])

    wifi_rate = RadioField(label="Wifi Rating",
                           validators=[DataRequired()],
                           choices=["💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪", "✘"])

    power_rating = RadioField(label="Power Outlet Rating",
                              validators=[DataRequired()],
                              choices=["🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌", "✘"])

    submit = SubmitField(label='Add new Cafe')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with app.app_context():
            db.session.add(cafe(
                cafe_name=str(form.cafe.data),
                location_url=str(form.location_url.data),
                open_time=str(form.open.data),
                close_time=str(form.close.data),
                coffee_rating=str(form.coffee_rate.data),
                wifi_rating=str(form.wifi_rate.data),
                power_rating=str(form.power_rating.data)
            ))
            db.session.commit()
        return redirect("/cafes")
    return render_template('add.html', form=form)


# @app.route('/cafes')
# def cafes():
#     with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
#         csv_data = csv.reader(csv_file, delimiter=',')
#         list_of_rows = []
#         for row in csv_data:
#             list_of_rows.append(row)
#     return render_template('cafes.html', cafes=list_of_rows)

@app.route('/cafes')
def cafes():
    list_of_rows = db.session.execute(db.select(cafe).order_by(cafe.id)).scalars()
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
