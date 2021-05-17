import time
import uuid

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


@api.route('/<string:input>', methods=['GET'])
def get_by_id(input):
    all_order = [x.json() for x in models.Order.query.all()]
    for data in all_order:
        data["user"] = models.User.get_by_id(data['user_id']).json()

    # get order for user
    for data in all_order:
        rs = []
        query = models.User.get_all_detail(data['id'])
        for i in query:
            result = {'id': i[1], 'description': i[2], 'amount': i[3], 'price': i[4], 'total': (i[3] * i[4])}
            rs.append(result)
        data["items"] = rs

    # get order user by id_user or name_user
    a = []
    for data in all_order:
        if data['id'] == input:
            if data['status'] == "pending" or data['status'] == "confirmed":
                data['created_date'] = time.time()
            a.append(data)
    return send_result(a)


@api.route('/', methods=["POST"])
def create_order():
    data = reqparse.request.get_json()
    order = models.Order(id=str(uuid.uuid1()), **data)
    try:
        order.save_to_db()
        return send_result(order.json())
    except:
        return send_error()


@api.route('/stt/<string:status>', methods=['GET'])
def get_by_stt(status):
    rs = []
    x = [x.json() for x in models.Order.query.all()]
    for data in x:
        data["user"] = models.User.get_by_id(data['user_id']).json()
    for data in x:
        if data['status'] == status:
            rs.append(data)
    return send_result(rs)


@api.route('/<int:_id>', methods=['PUT'])
def put_status(_id):
    data = reqparse.request.get_json()

    order = models.Order.find_by_id(_id)
    if order is None:
        send_error()
    else:
        # order.status = data['status']

        keys = ["status", "created_date"]
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


@api.route('/date', methods=['GET'])
def get_by_date():
    a = []
    all_order = [x.json() for x in models.Order.query.all()]
    for data in all_order:
        data["user"] = models.User.get_by_id(data['user_id']).json()
    start = request.args.get('start', 1617210000, type=int)
    end = request.args.get('end', 1619715600, type=int)

    for data in all_order:
        if data['created_date'] >= start:
            if data['created_date'] <= end:
                a.append(data)
    return send_result(a)


@api.route('/make_invoice/<int:_id>', methods=['PUT'])
def put_make_invoice(_id):
    data = reqparse.request.get_json()

    order = models.Order.find_by_id(_id)
    if order is None:
        send_error()
    else:
        order.make_invoice = data['make_invoice']
        order.created_date = time.time()
        order.status = "completed"
        db.session.commit()
    return send_result(order.json())
