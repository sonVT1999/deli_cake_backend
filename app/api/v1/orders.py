from flask import Blueprint, request
from flask_restful import reqparse

from app import models
from app.extensions import db
from app.utils import send_result, send_error

api = Blueprint('orders', __name__)


@api.route('', methods=['GET'])
def get_all():
    all_order = [x.json() for x in models.Order.query.all()]
    for data in all_order:
        data["user"] = models.User.get_by_id(data['user_id']).json()

    return send_result(all_order)


@api.route('/stt/<string:status>', methods=['GET'])
def get_by_stt(status):
    rs = []
    x = [x.json() for x in models.Order.query.all()]

    for data in x:
        if data['status'] == status:
            rs.append(data)
    return send_result(rs)


@api.route('/<int:_id>', methods=['PUT'])
def put_by_id(_id):
    data = reqparse.request.get_json()

    order = models.Order.find_by_id(_id)
    if order is None:
        send_error()
    else:
        keys = ["total", "created_date", "status", "user_id", "voucher", "tax", "make_invoice"]
        for key in keys:
            if key in data.keys():
                setattr(order, key, data[key])
        db.session.commit()
    return send_result(order.json())


@api.route('/', methods=['DELETE'])
def delete_by_id():

    ids = request.args.getlist('ids', type=str)
    for i in ids:
        order = models.Order.find_by_id(i)
        if order.status == "pending" or order.status == "confirmed":
            return send_error(message="order not delete!")
        if order:
            order.delete_to_db()
    return send_result(message="deleted successfully!")
