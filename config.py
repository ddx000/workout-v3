import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_admin import Admin

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

admin = Admin(app, name='microblog', template_mode='bootstrap3')

print("##########2")
# Build the Sqlite ULR for SqlAlchemy
# three slash for windows
sqlite_url = "sqlite:///" + os.path.join(basedir, "people.db")

print(sqlite_url)

# Configure the SqlAlchemy part of the app instance
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create the SqlAlchemy db instance
db = SQLAlchemy(app)
print("##########3")
# Initialize Marshmallow
ma = Marshmallow(app)
