from flask import Flask
from resources.penguins import penguins
import models
DEBUG = True
PORT = 8000
app = Flask(__name__)

# ==============================
# 			REGISTER BLUEPRINTS
# ==============================

# Penguins
app.register_blueprint(penguins, url_prefix='/api/v1/penguins')

# ==============================
# 						ROUTES
# ==============================

# Index
@app.route('/')
def index():
	return 'Hello, Penguin World!'

# ==============================
# 					CONNECTION
# ==============================
if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT) 