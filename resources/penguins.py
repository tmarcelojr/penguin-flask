import models
from flask import Blueprint

# ==============================
# 					BLUEPRINT
# ==============================

penguins = Blueprint('penguins', 'penguins')

# Index
@penguins.route('/', methods=['GET'])
def test_penguin_resource():
	return "We have a resource for penguins!"