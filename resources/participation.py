from models import Participation, Baby_Penguin
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict

# ==============================
# 					BLUEPRINT
# ==============================

participation = Blueprint('participation', 'participation')

# ==============================
# 						ROUTES
# ==============================

# Participation index
@participation.route('/', methods=['GET'])
@login_required
def participation_index():
	print('this is our current user', current_user)
	#  getting an error because we are claling on current_user not baby_penguin
	current_participation_dicts = [model_to_dict(participant) for participant in Participation.participant]
	return jsonify(
			data=current_participation_dicts,
			message=f'Successfully retrieved {len(current_participation_dicts)} current participated activities.',
			status=200
		), 200

# Participate
@participation.route('/<participant_id>', methods=['POST'])
@login_required
def participate(participant_id):
	payload = request.get_json()
	baby_penguin_participate = Participation.create(
			participant=participant_id
		)
	participation_dict = model_to_dict(baby_penguin_participate)

	return jsonify(
			data=participation_dict,
			message=f'Succesfully signed up baby penguin.',
			status=201
		), 201