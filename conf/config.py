import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_admin import Admin
from flask_cors import CORS

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

CORS(app)


admin = Admin(app, name='microblog', template_mode='bootstrap3')

# Build the Sqlite ULR for SqlAlchemy
# three slash for windows
sqlite_url = "sqlite:///" + os.path.join(basedir, "testsqlite.db")

# Configure the SqlAlchemy part of the app instance
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "test_app"
app.config['CORS_HEADERS'] = 'Content-Type'

# Create the SqlAlchemy db instance
db = SQLAlchemy(app)
# Initialize Marshmallow
ma = Marshmallow(app)


print("### init db and marshmallow ###")
