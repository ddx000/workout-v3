"""
Main module of the server file
"""

# 3rd party moudles
from flask import render_template

# Local modules
import config

from flask_cors import CORS
# Get the application instance
connex_app = config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")

CORS(connex_app.app)


# # Create a URL route in our application for "/"
# @connex_app.route("/")
# def home():
#     """
#     This function just responds to the browser URL
#     localhost:5000/

#     :return:        the rendered template "home.html"
#     """
#     return render_template("home.html")


# @connex_app.app.after_request
# def after_request(response):
#     print("after request")
#     header = response.headers
#     header['Access-Control-Allow-Origin'] = '*'
#     print(response)
#     return response


if __name__ == "__main__":
    connex_app.run(debug=True)
