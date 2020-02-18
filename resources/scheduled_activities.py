from models import Scheduled_Activity
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict

# ==============================
# 					BLUEPRINT
# ==============================

scheduled_activities = Blueprint('scheduled_activities', 'scheduled_activities')

# ==============================
# 						ROUTES
# ==============================

# Scheduled Activities index
@scheduled_activities.route('/', methods=['GET'])
@login_required
def scheduled_activities_index():
	scheduled_activities_dicts = [model_to_dict(scheduled_activity) for scheduled_activity in current_user.scheduled_activities]
	return jsonify(
			data=scheduled_activities_dicts,
			message=f'Successfully retrieved {len(scheduled_activities_dicts)} scheduled activities.',
			status=200
		), 200

# Schedule activity
# specify which activity I'm setting in the params
@scheduled_activities.route('/<activity_id>', methods=['POST'])
@login_required
def create_scheduled_activity(activity_id):
	payload = request.get_json() # activity ID could be here
	scheduled_activity = Scheduled_Activity.create(
			activity=activity_id,
			parent=current_user.id
		)
	scheduled_activity_dict = model_to_dict(scheduled_activity)
	scheduled_activity_dict['parent'].pop('password')

	return jsonify(
			data=scheduled_activity_dict,
			message=f"Successfully scheduled activity by {current_user.id}.",
			status=201
		), 201

# Delete scheduled activity
@scheduled_activities.route('/<id>', methods=['Delete'])
@login_required
def delete_scheduled_activity(id):
	scheduled_activity_to_delete = Scheduled_Activity.get_by_id(id)
	if current_user.id == scheduled_activity_to_delete.parent.id:
		scheduled_activity_to_delete.delete_instance()
		return jsonify(
      data={}, 
      message=f'Successfully deleted activity with id {scheduled_activity_to_delete.parent.id}',
      status=200
    ), 200
	else:
		return jsonify(
				data={'Error: Forbidden'},
				message='Penguins can only delete their own activity.',
				status=403
			), 403
