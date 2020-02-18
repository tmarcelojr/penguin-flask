from models import Activity
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
	scheduled_activities_dicts = [model_to_dict(scheduled_activities) for scheduled_activity in current_user.scheduled_activities]
	return jsonify(
			data=scheduled_activities_dicts,
			message=f'Successfully retrieved {len(scheduled_activities_dicts)} scheduled activities.',
			status=200
		), 200

# Schedule activity
@scheduled_activities.route('/', methods=['POST'])
@login_required
def create_scheduled_activity():
	payload = request.get_json()
	activity = Activity.create(
			scheduler=current_user.id
		)
	scheduled_activity_dict = model_to_dict(activity)
	scheduled_activity_dict['scheduler'].pop('password')

	return jsonify(
			data=scheduled_activity_dict,
			message=f"Successfully scheduled activity by {payload['scheduler']}.",
			status=201
		), 201
