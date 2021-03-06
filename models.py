# Python interaction with our OS
import os
# Authentication, sessions, & User model
from flask_login import UserMixin
# * imports everything from peewee
from peewee import *

import datetime

# Peewee extension for creating a DB connection from a URL string
from playhouse.db_url import connect

# ===================================
# CONNECTION TO HEROKU DB OR LOCAL DB
# ===================================

if 'ON_HEROKU' in os.environ: # later we will manually add this env var 
                              # in heroku so we can write this code
  DATABASE = connect(os.environ.get('DATABASE_URL')) # heroku will add this 
                                                     # env var for you 
                                                     # when you provision the
                                                     # Heroku Postgres Add-on
else:
  DATABASE = SqliteDatabase('dogs.sqlite')

  # OPTIONALLY: instead of the above line, here's how you could have your 
  # local app use PSQL instead of SQLite:

  # DATABASE = PostgresqlDatabase('dog_demo', user='reuben')  

  # the first argument is the database name -- YOU MUST MANUALLY CREATE 
  # IT IN YOUR psql TERMINAL
  # the second argument is your Unix/Linux username on your computer

# ==============================
# 				CREATE DATABASE
# ==============================

DATABASE = SqliteDatabase('baby_penguins.sqlite')
DATABASE = SqliteDatabase('activities.sqlite')
DATABASE = SqliteDatabase('scheduled_activities.sqlite')

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
  DATABASE.create_tables([Penguin, Baby_Penguin, Activity, Scheduled_Activity], safe=True)
  print("Connected to DB and created tables if they weren't already there")
  DATABASE.close()







