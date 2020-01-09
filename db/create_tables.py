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


# class User(Base):

# 	__tablename__ = "user"

# 	id = Column(Integer, primary_key=True)
# 	first_name = Column(String(128))
# 	last_name = Column(String(128))
# 	email = Column(String(256))
# 	password_hash = Column(String(128))
# 	description = Column(String)
# 	link = Column(String)

# 	def set_password(self, password):
# 		self.password_hash = generate_password_hash(password)

# 	def check_password(self, password):
# 		return check_password_hash(password, self.password_hash)


# class Student(Base):
# 	__tablename__ = "students"
# 	id = Column(Integer, primary_key=True)
# 	first_name = Column(String(128))
# 	last_name = Column(String(128))
# 	email = Column(String(256))
# 	password_hash = Column(String(2048))
# 	description = Column(String)
# 	link = Column(String)
# 	school_name	= Column(String)

# 	def set_password(self, password):
# 		self.password_hash = bcrypt.hashpw(password, bcrypt.gensalt()).decode()

# 	def __repr__(self):
# 		return "<Student(first_name='%s', last_name='%s', email='%s', \
# 		school_name='%s', description='%s', link='%s'>" \
# 		% (self.first_name, self.last_name, self.email, self.school_name ,self.description, self.link)

# class Employer(Base):
# 	__tablename__ = "employers"
# 	id = Column(Integer, primary_key=True)
# 	first_name = Column(String(128))
# 	last_name = Column(String(128))
# 	email = Column(String(256))
# 	password_hash = Column(String(2048))
# 	description = Column(String)
# 	link = Column(String)
# 	company_name = Column(String)

# 	def set_password(self, password):
# 		temp_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
# 		print(temp_hash)
# 		print(type(temp_hash))
# 		self.password_hash = temp_hash

# 	def __repr__(self):
# 		return "<Student(first_name='%s', last_name='%s', email='%s', \
# 		company_name='%s', description='%s', link='%s'>" \
# 		% (self.first_name, self.last_name, self.email, self.company_name ,self.description, self.link)


if __name__ == "__main__":
	Base.metadata.create_all(engine)
