from models import Activity
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict

# ==============================
# 					BLUEPRINT
# ==============================

activities = Blueprint('activities', 'activities')

# ==============================
# 						ROUTES
# ==============================

# Activities index
@activities.route('/', methods=['GET'])
@login_required
def activities_index():
	activities_dicts = [model_to_dict(activities) for activity in current_user.activities]
	return jsonify(
			data=activities_dicts,
			message=f'Successfully retrieved {len(activities_dicts)} activities.',
			status=200
		), 200

# Create activity
@activities.route('/', methods=['POST'])
@login_required
def create_activity():
	payload = request.get_json()
	activity = Activity.create(
			name=payload['name'],
			description=payload['description'],
			creator=current_user.id
		)
	activity_dict = model_to_dict(activity)
	activity_dict['creator'].pop('password')

	return jsonify(
			data=activity_dict,
			message=f"Successfully created activity {payload['name']}.",
			status=201
		), 201

# Delete activity
@activities.route('/<id>', methods=['Delete'])
@login_required
def delete_activity(id):
	activity_to_delete = Activity.get_by_id(id)
	if current_user.id == activity_to_delete.creator.id:
		activity_to_delete.delete_instance()
		return jsonify(
      data={}, 
      message=f'Successfully deleted activity with id {activity_to_delete.creator.id}',
      status=200
    ), 200
	else:
		return jsonify(
				data={'Error: Forbidden'},
				message='Penguin can only delete their own activities.',
				status=403
			), 403

# Update activity
@activities.route('/<id>', methods=['PUT'])
@login_required
def update_actvity(id):
	payload = request.get_json()
	activity = Activity.get_by_id(id)
	if current_user.id == activity.creator.id:
		activity.name = payload['name'] if 'name' in payload else None
		activity.save()
		activity_dict = model_to_dict(activity)
		return jsonify(
				data=activity_dict,
				message=f'Successfully updated activity with id {activity.id}.',
				status=200
			), 200
	else:
		return jsonify(
				data='Error: Forbidden',
				message='Penguins can only update their own activity.',
				status=403
			), 403


