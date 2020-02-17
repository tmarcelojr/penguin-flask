from models import Penguin, DoesNotExist
from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash
from playhouse.shortcuts import model_to_dict

# ==============================
# 					BLUEPRINT
# ==============================

penguins = Blueprint('penguins', 'penguins')

# ==============================
# 						ROUTES
# ==============================

# Index
@penguins.route('/', methods=['GET'])
def test_penguin_resource():
	return "We have a resource for penguins!"

# Register Penguin
@penguins.route('/register', methods=['POST'])
def register():
	payload = request.get_json()
	# lowecare usernames
	payload['username'] = payload['username'].lower()

	try:
		# Check if username is taken
		Penguin.get(Penguin.username == payload['username'])
		return jsonify(
				data={},
				message='Username is already taken.',
				status=401
			), 401
	except DoesNotExist:
		created_penguin = Penguin.create(
				username=payload['username'],
				password=generate_password_hash(payload['password'])
			)

		penguin_dict = model_to_dict(created_penguin)
		# Do not return password
		penguin_dict.pop('password')
		return jsonify(
				data=penguin_dict,
				message=f"Successfully registed {penguin_dict['username']}.",
				status=201
			), 201




