# Import modules
import os

import json

from db.create_tables import Event, StudentUnion, User, Letter

import bcrypt

from flask import Flask, render_template, request
import flask
import flask_login 

from werkzeug.security import generate_password_hash, check_password_hash

from cryptography.fernet import Fernet

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from datetime import datetime



# Postgres
engine = create_engine(os.environ["DATABASE_URL"], echo = True)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


# Flask app
app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = dict()
for user in session.query(User):
	users[user.email] = {"password_hash": user.password_hash}

class FlaskUser(flask_login.UserMixin):
	
	def __init__(self):
		self.is_authenticated_local = False

	def set_is_authenticated(self, value):
		self.is_authenticated_local = value

@login_manager.user_loader
def user_loader(email):
	if email not in users:
		return
	user = FlaskUser()
	user.id = email
	return user

@login_manager.request_loader
def request_loader(request):

	email = request.form.get("email")
	if email not in users:
		return

	user = FlaskUser()
	user.id = email

	password = request.form["password"]

	if bcrypt.checkpw(password.encode(), \
			session.query(Employer).filter_by(email=email).first().password_hash.encode()):
		user.set_is_authenticated(True)
	else:
		user.set_is_authenticated(False)
	return user


@app.route("/")
def home():
	return_dict = dict()
	return_dict["name"] = list()
	return_dict["datetime_start"] = list()
	return_dict["website"] = list()
	for event in session.query(Event).order_by("datetime_start"):
		return_dict["name"].append(event.name)
		return_dict["datetime_start"].append(event.datetime_start.strftime("%A, %B %d, %Y"))
		return_dict["website"].append(event.website)
		print(event.id, event.name)
	return render_template("home.html", data=return_dict)

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/events")
def events():
	return_dict = dict()
	return_dict["name"] = list()
	return_dict["datetime_start"] = list()
	return_dict["website"] = list()
	for event in session.query(Event).order_by("datetime_start"):
		return_dict["name"].append(event.name)
		return_dict["datetime_start"].append(event.datetime_start.strftime("%A, %B %d, %Y"))
		return_dict["website"].append(event.website)
		print(event.id, event.name)
	return render_template("events.html", data=return_dict)

@app.route("/initiatives")
def initiatives():
	return render_template("initiatives.html")

@app.route("/contact")
def contact():
	return render_template("contact.html")

@app.route("/speed_dating_form")
def speed_dating_form():
	return render_template("speed_dating_form.html")

@app.route("/create_letter", methods=["GET", "POST"])
def create_letter():
	if request.method == "POST":
		print(request.form)
		letter = Letter(name=request.form["name"],
						email=request.form["email"],
						letter=request.form["letter"],
						cegep=request.form["cegep"],
						notes=request.form["notes"],
						creation_date=datetime.now())
		if request.form["share_identity"] == "False":
			letter.share_identity=False 
		elif request.form["share_identity"] == "True":
			letter.share_identity=True
		session.add(letter)
		session.commit()
		return "Letter sent! <a href=\"/speed_dating_form\">Write another response</a>"

@app.route("/create_event", methods=["GET", "POST"])
def create_event():
	if request.method == "POST":
		if request.form["password"] == os.environ["ADMIN_PASSWORD"]:
			print(request.form)
			event = Event(name=request.form["name"],
				location=request.form["location"],
				website=request.form["website"],
				datetime_start=request.form["datetime_start"],
				datetime_end=request.form["datetime_end"],
				student_union_name=request.form["student_union"],
				)
			session.add(event)
			session.commit()
			return "Succes! <a href='/'>Home</a>"
		else:
			return "WRONG PASSWORD"

	return render_template("create_event.html")

@app.route("/check_letters")
def check_letters():
	counter = 1
	return_txt = ''
	for letter in session.query(Letter):
		return_txt += "<p><b>%s</b> %s %s %s %s %s</p>" %(counter, letter.letter, letter.share_identity, letter.name, letter.notes, letter.cegep)
		counter += 1
	return return_txt

@app.route("/check_letters_edit")
def check_letters_edit():
	return_dict = dict()
	return_dict["id"] = list()
	return_dict["content"] = list()
	return_dict["cegep"] = list()

	for letter in session.query(Letter):
		return_dict["id"].append(letter.id)
		return_dict["content"].append(letter.letter + ' ' + letter.notes)
		return_dict["cegep"].append(letter.cegep)

	return render_template("check_letters.html", data=return_dict)

@app.route("/billboard")
def billboard():
	return render_template("billboard.html")


if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=5000)