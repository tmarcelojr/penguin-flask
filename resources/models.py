# Authentication, sessions, & User model
from flask_login import UserMixin
# * imports everything from peewee
from peewee import *
DATABASE = SqliteDatabase('penguins.sqlite')

# ==============================
# 						MODELS
# ==============================

# Penguin
class Penguin(UserMixin, Model):
  username = CharField(unique=True)
  password = CharField()
  type_of_penguin = CharField()

  class Meta: 
    database = DATABASE

# Baby Penguin
class Baby_Penguin(Model):
	name = CharField(unique=True)
	parent = ForeignKeyField(Penguin, backref='baby_penguins')
	type_of_penguin = CharField()

	class Meta:
		database = DATABASE

# Activity
class Activity(Model):
	name = CharField()
	description = Charfield()

	class Meta:
		database = DATABASE

# Scheduled Activity
class Scheduled_Activity(Model):
	creator = ForeignKeyField(Penguin, backref='scheduled_activities')

	class Meta:
		database = DATABASE

# Participation
class Participation(Model):
	participant = ForeignKeyField(Baby_Penguin, backref='participation')

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







