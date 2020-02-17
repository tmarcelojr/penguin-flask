from flask import Flask
import models
DEBUG = True
PORT = 8000
app = Flask(__name__)

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