# -*- coding: utf-8 -*-

import traceback
from time import strftime

from flask import Flask, request
from flask_cors import CORS

from app.extensions import jwt, logger, db, ma
from .api import v1 as api_v1
from .settings import ProdConfig


def create_app(config_object=ProdConfig):
    """
    Init App
    :param config_object:
    :return:
    """
    app = Flask(__name__, static_url_path="", static_folder="./files")
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    CORS(app)

    return app


def register_extensions(app):
    """
    Init extension
    :param app:
    :return:
    """
    # Order matters: Initialize SQLAlchemy before Marshmallow
    db.app = app
    db.init_app(app)  # SQLAlchemy
    ma.init_app(app)  # Marshmallow json parser and validator
    jwt.init_app(app)

    @app.after_request
    def after_request(response):
        """

        :param response:
        :return:
        """
        # This IF avoids the duplication of registry in the log, since that 500 is already logged via @app.errorhandler.
        if response.status_code != 500:
            ts = strftime('[%Y-%b-%d %H:%M]')
            logger.error('%s %s %s %s %s %s',
                         ts,
                         request.remote_addr,
                         request.method,
                         request.scheme,
                         request.full_path,
                         response.status)
        return response

    @app.errorhandler(Exception)
    def exceptions(e):
        """
        Handling exceptions
        :param e:
        :return:
        """
        ts = strftime('[%Y-%b-%d %H:%M]')
        tb = traceback.format_exc()
        message = "5xx INTERNAL SERVER ERROR"
        error = '{} {} {} {} {} {} {} \n{}'.format(ts, request.remote_addr, request.method, request.scheme,
                                                   request.full_path, message, str(e), tb)
        logger.error(error)

        return "Internal Server Error", 500


def register_blueprints(app):
    """
    Init blueprint for api url
    :param app:
    :return:
    """
    app.register_blueprint(api_v1.auth.api, url_prefix='/api/v1/auth')
    app.register_blueprint(api_v1.items.api, url_prefix='/api/v1/items')
    app.register_blueprint(api_v1.orders.api, url_prefix='/api/v1/orders')
    app.register_blueprint(api_v1.orders_details.api, url_prefix='/api/v1/orders_details')
    app.register_blueprint(api_v1.categories.api, url_prefix='/api/v1/categories')
    app.register_blueprint(api_v1.subcategories.api, url_prefix='/api/v1/subcategories')
    app.register_blueprint(api_v1.recipes.api, url_prefix='/api/v1/recipes')
    app.register_blueprint(api_v1.users.api, url_prefix='/api/v1/users')
    app.register_blueprint(api_v1.images_items.api, url_prefix='/api/v1/images_items')
    app.register_blueprint(api_v1.images_recipes.api, url_prefix='/api/v1/images_recipes')



