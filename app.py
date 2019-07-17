"""Application factory"""

# Third party library
from flask import Flask, jsonify

# local imports
from config import app_config
from database import db, migrate


def create_app(env):
	"""Flask application factory"""

	# initialization the application
	app = Flask(__name__)
	app.config.from_object(app_config[env])

	# binding the database and migrate to the flask app instance
	db.init_app(app)
	migrate.init_app(app, db)

	# Models
	import database.models

	# root
	@app.route('/', methods=['GET'])
	def index():
		"""Index route for the API"""
		return jsonify(
				status='Healthy',
		)

	# return because of test.
	return app
