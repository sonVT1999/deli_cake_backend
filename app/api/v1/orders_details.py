import uuid

from flask import Blueprint
from flask_restful import reqparse

from app import models
from app.utils import send_result, send_error

api = Blueprint('orders_details', __name__)


@api.route('/', methods=["POST"])
def create_order_detail():
    data = reqparse.request.get_json()
    order_detail = models.Order_detail(id=str(uuid.uuid1()), **data)
    try:
        order_detail.save_to_db()
        return send_result(order_detail.json())
    except:
        return send_error()
