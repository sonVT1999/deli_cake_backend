import uuid

from flask import Blueprint, request
from flask_restful import reqparse

from app import models
from app.utils import send_error, send_result

api = Blueprint('subcategories', __name__)


@api.route('/', methods=["POST"])
def create_cate():
    data = reqparse.request.get_json()
    item = models.Subcategory(id=str(uuid.uuid1()), **data)
    try:
        item.save_to_db()
        return send_result(item.json())
    except:
        return send_error()


@api.route('/', methods=['DELETE'])
def delete_by_id():
    _id = request.args.get('_id', type=str)
    subcate = models.Subcategory.get_by_id(_id)
    if subcate:
        subcate.delete_to_db()
    return send_result(message="deleted successfully!")