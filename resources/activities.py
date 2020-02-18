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
