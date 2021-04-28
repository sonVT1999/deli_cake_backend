from flask import Blueprint

from app.utils import send_result

api = Blueprint('auth', __name__)


@api.route('/login', methods=['POST'])
def login():
    """ This is controller of the login api

    Requests Body:

    Returns:

    Examples::

    """

    data = {
        'access_token': "access_token",
        'refresh_token': "refresh_token",
        'username': "username",
        'user_id': "id",
        'display_name': "display_name"
    }

    return send_result(data=data, message="Logged in successfully!")


@api.route('/logout', methods=['POST'])
def logout():
    """ This is controller of the logout api

    Requests Body:

    Returns:

    Examples::

    """

    data = {
        'display_name': "display_name"
    }

    return send_result(data=data, message="logout in successfully!")
