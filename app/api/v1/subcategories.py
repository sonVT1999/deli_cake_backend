import uuid

from flask import Blueprint
from flask_restful import reqparse

from app import models
from app.utils import send_error, send_result

api = Blueprint('subcategories', __name__)


@api.route('/', methods=["POST"])
def create_cate():
    data = reqparse.request.get_json()
    item = models.Item(id=str(uuid.uuid1()), **data)
    try:
        item.save_to_db()
        return send_result(item.json())
    except:
        return send_error()
