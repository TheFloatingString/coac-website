# Import modules
import os

import json

from db.create_tables import Event, StudentUnion, User
from src import read_credentials

import bcrypt

from flask import Flask, render_template, request
import flask
import flask_login 

from werkzeug.security import generate_password_hash, check_password_hash

from cryptography.fernet import Fernet

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from datetime import datetime


env_keys = read_credentials.return_keys()

# Postgres
engine = create_engine(env_keys["DATABASE_URL"], echo = True)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


# Flask app
app = Flask(__name__)
app.secret_key = env_keys["SECRET_KEY"]

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

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=5000)