import os

import sys
print(sys.path)

from flask import Flask
from .api import GatherJobPosts
from flask_restful import Api

from .pages import pages_bp

def init_routes(api):
	api.add_resource(GatherJobPosts,"/api/GatherJobPosts")

def create_app(test_config = None):
        app = Flask(__name__,instance_relative_config = True)
        api = Api(app)
        init_routes(api)
        app.register_blueprint(pages_bp)

        return app
