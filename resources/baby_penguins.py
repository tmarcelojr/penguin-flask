from models import Baby_Penguin
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict

# ==============================
# 					BLUEPRINT
# ==============================

baby_penguins = Blueprint('baby_penguins', 'baby_penguins')

# ==============================
# 						ROUTES
# ==============================

# Baby penguins index
@baby_penguins.route('/', methods=['GET'])
@login_required
def baby_penguins_index():
	penguin_current_baby_penguins_dicts = [model_to_dict(penguin) for penguin in current_user.baby_penguins]
	return jsonify(
			data=penguin_current_baby_penguins_dicts,
			message=f'Successfully retrieved {len(penguin_current_baby_penguins_dicts)} baby penguins',
			status=200
		), 200

# Create baby penguin
@baby_penguins.route('/', methods=['POST'])
@login_required
def create_baby_penguin():
	payload = request.get_json()
	baby_penguin = Baby_Penguin.create(
			name=payload['name'],
			parent=current_user.id
		)

	print(baby_penguin)
	print(baby_penguin.__dict__)
	baby_penguin_dict = model_to_dict(baby_penguin)
	baby_penguin_dict['parent'].pop('password')

	return jsonify(
			data=baby_penguin_dict,
			message=f"Successfully created baby penguin {payload['name']}.",
			status=201
		), 201

# Delete baby penguin
@baby_penguins.route('/<id>', methods=['Delete'])
@login_required
def delete_baby_penguin(id):
	baby_penguin_to_delete = Baby_Penguin.get_by_id(id)
	if current_user.id == baby_penguin_to_delete.parent.id:
		baby_penguin_to_delete.delete_instance()
		return jsonify(
      data={}, 
      message=f'Successfully deleted baby penguin with id {baby_penguin_to_delete.parent.id}',
      status=200
    ), 200
	else:
		return jsonify(
				data={'Error: Forbidden'},
				message='Penguins can only delete their own baby penguins.',
				status=403
			), 403

# Update baby penguin
@baby_penguins.route('/<id>', methods=['PUT'])
@login_required
def update_baby_penguin(id):
	payload = request.get_json()
	baby_penguin = Baby_Penguin.get_by_id(id)
	if current_user.id == baby_penguin.parent.id:
		baby_penguin.name = payload['name'] if 'name' in payload else None

		# .save() allows updating properties
		baby_penguin.save()
		baby_penguin_dict = model_to_dict(baby_penguin)
		return jsonify(
				data=baby_penguin_dict,
				message=f'Successfully updated baby penguin with id {baby_penguin.id}.',
				status=200
			), 200
	else:
		return jsonify(
				data='Error: Forbidden',
				message='Penguins can only update their own baby penguin.',
				status=403
			), 403











