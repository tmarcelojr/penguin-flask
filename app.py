from flask import Flask, jsonify, g
from flask_login import LoginManager
from resources.penguins import penguins
from resources.baby_penguins import baby_penguins
from resources.activities import activities
from resources.scheduled_activities import scheduled_activities
from models import Penguin, DoesNotExist, initialize, DATABASE, Activity
DEBUG = True
PORT = 8000
app = Flask(__name__)

# ==============================
# 				LOGIN MANAGER
# ==============================
app.secret_key = 'This is our penguin club.'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
  try:
    return Penguin.get(Penguin.id == userid)
  except DoesNotExist:
    return None

# ==============================
# 			REGISTER BLUEPRINTS
# ==============================

# Penguins
app.register_blueprint(penguins, url_prefix='/api/v1/penguins')

# Baby penguins
app.register_blueprint(baby_penguins, url_prefix='/api/v1/baby_penguins')

# Activities
app.register_blueprint(activities, url_prefix='/api/v1/activities')

# Scheduled Activities
app.register_blueprint(scheduled_activities, url_prefix='/api/v1/scheduled_activities')

# ==============================
# 			DATABASE CONNECTION
# ==============================

@app.before_request
def before_request():
  g.db = DATABASE
  g.db.connect()


@app.after_request
def after_request(response):
  g.db.close()
  return response

# ==============================
# 						ROUTES
# ==============================

# Index
@app.route('/')
def index():
	return 'Hello, Penguin World!'

# ==============================
# 			CONNECTION TO SERVER
# ==============================
if __name__ == '__main__':
	initialize()
	app.run(debug=DEBUG, port=PORT) 