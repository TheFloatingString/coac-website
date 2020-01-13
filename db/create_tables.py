from sqlalchemy import Table, Column, Integer, Float, String, MetaData, DateTime
from sqlalchemy	import create_engine
from sqlalchemy.ext.declarative import declarative_base
import os

from werkzeug.security import generate_password_hash, check_password_hash

import bcrypt
import uuid

import random

engine = create_engine(os.environ["DATABASE_URL"], echo=True)

meta = MetaData()
Base = declarative_base()

print("tables loaded")

class Event(Base):
	__tablename__ = "events"

	id = Column(Integer, primary_key=True, unique=True, nullable=False, default=random.randint(0,2**30))
	name = Column(String, nullable=False)
	creator_id = Column(Integer)
	creator_name = Column(String)

	location = Column(String)
	student_union_name = Column(String)
	website = Column(String)
	description = Column(String)

	datetime_start = Column(DateTime)
	datetime_end = Column(DateTime)

	creation_date = Column(DateTime)
	modified_date = Column(DateTime)

	def __repr__(self):
		return "<Event()>" \
		% (self.name)

class StudentUnion(Base):
	__tablename__ = "student_unions"

	id = Column(Integer, primary_key=True, unique=True, nullable=False, default=int(uuid.uuid4()))
	name = Column(String)

class User(Base):
	__tablename__ = "user"
	id = Column(Integer, primary_key=True, unique=True, nullable=False, default=int(uuid.uuid4()))
	email = Column(String)
	first_name = Column(String)
	last_name = Column(String)
	password_hash = Column(String)

	role = Column(String)
	description = Column(String)
	website = Column(String)
	student_union = Column(String)

	creation_date = Column(DateTime)
	modified_date = Column(DateTime)

	def set_password(self, password):
		self.password_hash = generate_password_hash

	def check_password(self, password):
		return check_password_hash(password, self.password_hash)


if __name__ == "__main__":
	Base.metadata.create_all(engine)
