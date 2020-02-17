import models
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict

baby_penguins = Blueprint('baby_penguins', 'baby_penguins')

@baby_penguins.route('/', methods=['GET'])
@login_required
def baby_penguins_index():
	penguin_current_baby_penguins_dicts = [model_to_dict(penguin) for penguin in current_user.baby_penguins]
	return jsonify(
			data=penguin_current_baby_penguins_dicts,
			message=f'Successfully retrieved {len(penguin_current_baby_penguins_dicts)} baby penguins',
			status=200
		), 200