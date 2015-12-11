from flask import Flask
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
app.config.from_object('guacamole.config')
app.config.from_envvar('CONFIG', silent=True)

db_client = PyMongo(app)

from guacamole import routes
