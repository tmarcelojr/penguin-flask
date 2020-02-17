from models import Penguin, DoesNotExist
from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
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
		login_user(created_penguin)
		penguin_dict = model_to_dict(created_penguin)
		# Do not return password
		penguin_dict.pop('password')
		return jsonify(
				data=penguin_dict,
				message=f"Successfully registered {penguin_dict['username']}.",
				status=201
			), 201

# Login
@penguins.route('/login', methods=['POST'])
def login():
	payload = request.get_json()
	payload['username'] = payload['username'].lower()
	try:
		penguin = Penguin.get(Penguin.username == payload['username'])
		penguin_dict = model_to_dict(penguin)
		password_is_good = check_password_hash(penguin_dict['password'], payload['password'])
		if password_is_good:
			login_user(penguin)
			penguin_dict.pop('password')
			return jsonify(
					data=penguin_dict,
	  			message=f"Successfully logged in as {penguin_dict['username']}",
	  			status=200
  			), 200
		else:
  		# This means password is not correct.
			return jsonify(
      	data={},
        message="Username or password is incorrect",
        status=401
      	), 401
	except DoesNotExist:
	# Username not correct
		return jsonify(
        data={},
        message="Username or password is incorrect",
        status=401
      ), 401

# Check current user
@penguins.route('/logged_in', methods=['GET'])
def get_logged_in_user():
  if not current_user.is_authenticated:
    return jsonify(
      data={},
      message="No user is currently logged in",
      status=401
    ), 401
  else:
    penguin_dict = model_to_dict(current_user)
    penguin_dict.pop('password')
    return jsonify(
      data=penguin_dict,
      message=f"Current user is {penguin_dict['username']}", 
      status=200
    ), 200

# Logout
@penguins.route('/logout', methods=['GET'])
def logout():
  logout_user()
  return jsonify(
    data={},
    message="Successfully logged out",
    status=200
  ), 200