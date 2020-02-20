# Authentication, sessions, & User model
from flask_login import UserMixin
# * imports everything from peewee
from peewee import *

import datetime

# ==============================
# 				CREATE DATABASE
# ==============================

DATABASE = SqliteDatabase('baby_penguins.sqlite')
DATABASE = SqliteDatabase('activities.sqlite')
DATABASE = SqliteDatabase('scheduled_activities.sqlite')
DATABASE = SqliteDatabase('participation.sqlite')

# ==============================
# 						MODELS
# ==============================

# Penguin
class Penguin(UserMixin, Model):
	username = CharField(unique=True)
	password = CharField()

	class Meta:
		database = DATABASE

# Baby Penguin
class Baby_Penguin(Model):
	name = CharField()
	parent = ForeignKeyField(Penguin, backref='baby_penguins')

	class Meta:
		database = DATABASE

# Activity
class Activity(Model):
	name = CharField()
	description = CharField()
	creator = ForeignKeyField(Penguin, backref='activities')

	class Meta:
		database = DATABASE

# Scheduled Activity
class Scheduled_Activity(Model):
	# change this to not created at but when it will happen 
	# created_at = DateTimeField(default=datetime.datetime.now)
	activity = ForeignKeyField(Activity, backref='scheduled_activities')
	parent = ForeignKeyField(Penguin, backref='scheduled_activities')
	participant = ForeignKeyField(Baby_Penguin, backref='scheduled_activities')

	class Meta:
		database = DATABASE

# ==============================
# 					CONNECTION
# ==============================

def initialize():
  DATABASE.connect()
  DATABASE.create_tables([Penguin, Baby_Penguin, Activity, Scheduled_Activity, Participation], safe=True)
  print("Connected to DB and created tables if they weren't already there")
  DATABASE.close()







