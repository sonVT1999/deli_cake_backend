import logging
import os
from logging.handlers import RotatingFileHandler

from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from webargs.flaskparser import FlaskParser

parser = FlaskParser()
jwt = JWTManager()

# init SQLAlchemy
db = SQLAlchemy()
ma = Marshmallow()

os.makedirs("logs", exist_ok=True)
app_log_handler = RotatingFileHandler('logs/app.log', maxBytes=1000000, backupCount=30)

# logger
logger = logging.getLogger('api')
logger.setLevel(logging.DEBUG)
logger.addHandler(app_log_handler)
