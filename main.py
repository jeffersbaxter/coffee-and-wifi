import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('APP_KEY')
Bootstrap(app)


def get_csv_data():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return list_of_rows


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    open_time = StringField('Opens', validators=[DataRequired()])
    close_time = StringField('Closes', validators=[DataRequired()])
    coffee = StringField('Coffee', validators=[DataRequired()])
    wifi = StringField('Wifi', validators=[DataRequired()])
    power = StringField('Power', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', mode='a', newline='') as f:
            writer = csv.writer(f)
            row = [form.cafe.data, form.location.data, form.open_time.data, form.close_time.data, form.coffee.data, form.wifi.data, form.power.data]
            writer.writerow(row)
        return render_template('index.html')
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    return render_template('cafes.html', cafes=get_csv_data())


if __name__ == '__main__':
    app.run(debug=True)
