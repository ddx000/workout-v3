"""
Main module of the server file
"""

# 3rd party moudles
from flask import render_template
from flask_cors import CORS


# Local modules
from conf import config

# Get the application instance
connex_app = config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")

# CORS(connex_app.app)

if __name__ == "__main__":
    connex_app.run(debug=True)
