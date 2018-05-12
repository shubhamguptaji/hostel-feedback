from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import sys
import datetime
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	email = Column(String(250), nullable=False)
	password_hash = Column(String(64))

	def hash_password(self, password):
		self.password_hash = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password_hash)


	@property
	def serialize(self):

		return {
		'id' : self.id,
		'name' : self.name,
		'email' :self.email,
		'picture' : self.picture,
		}

class Categories(Base):
	__tablename__ = 'categories'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	image = Column(String(250), nullable=False)
	description = Column(String(250), nullable=False)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):

		return {
		'name': self.name,
		'id' : self.id,
		}

class Feedback(Base):
	__tablename__ = 'feedback'

	name = Column(String(100), nullable=False)
	id = Column(Integer, primary_key=True)
	rating1 = Column(Integer, default=0)
	rating2 = Column(Integer, default=0)
	rating3 = Column(Integer, default=0)
	rating4 = Column(Integer, default=0)
	rating5 = Column(Integer, default=0)
	totalrating = Column(Integer, default=0)
	avgratings = Column(Float, default=0)
	categories_id = Column(Integer, ForeignKey('categories.id'))
	categories = relationship(Categories)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)


	@property
	def serialize(self):

		return {
		'name' : self.name,
		'description' : self.description,
		'id' : self.id,
		'rating' : self.rating,

		}

class Comments(Base):
	__tablename__ = 'comments'

	id = Column(Integer, primary_key=True)
	commentdata = Column(String(250), nullable=False)
	time = Column(String)
	rate = Column(Integer, default=0)
	categories_id = Column(Integer, ForeignKey('categories.id'))
	categories = relationship(Categories)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)
	feedback_id = Column(Integer, ForeignKey('feedback.id'))
	feedback = relationship(Feedback)


	
engine = create_engine(
	'sqlite:///problems.db')

Base.metadata.create_all(engine)