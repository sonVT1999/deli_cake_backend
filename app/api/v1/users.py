import uuid

from flask import Blueprint, request
from flask_restful import reqparse

from app import models
from app.utils import send_result, send_error

api = Blueprint('users', __name__)


# users = [
#     {'id': "1", 'name': "son", 'address': "Ha Noi", 'phone_number': "0987243623",
#      'email': "son@boot.ai", 'total': 504, 'created': 1615791600, 'order':
#          [
#              {"decription": 'matcha chess cake', "amount": '1', "price": 168, "total": 168, "voucher": 'False',
#               "tax": 'False'},
#              {"decription": 'matcha cake', "amount": '1', "price": 168, "total": 168, "voucher": 'False',
#               "tax": 'False'},
#              {"decription": 'chess cake', "amount": '1', "price": 168, "total": 168, "voucher": 'False',
#               "tax": 'False'}
#          ]
#      },
#     {'id': "2", 'name': "ha", 'address': "Thai Binh", 'phone_number': "0987243623",
#      'email': "han@boot.ai", 'total': 668, 'created': 1618475000, 'order':
#          [
#              {"decription": 'matcha chess cake', "amount": '1', "price": 168, "total": 168, "voucher": 'False',
#               "tax": 'False'},
#              {"decription": 'chocolate chess cake', "amount": '1', "price": 100, "total": 100, "voucher": 'False',
#               "tax": 'False'},
#              {"decription": 'chocolate cake', "amount": '2', "price": 200, "total": 400, "voucher": 'False',
#               "tax": 'False'}
#          ]
#      },
#     {'id': "3", 'name': "hao", 'address': "Ha Nam", 'phone_number': "0987243623",
#      'email': "hao@boot.ai", 'total': 600, 'created': 1615791600, 'order':
#          [
#              {"decription": 'banana cake', "amount": '1', "price": 100, "total": 100, "voucher": 'False',
#               "tax": 'False'},
#              {"decription": 'pine chess cake', "amount": '1', "price": 200, "total": 200, "voucher": 'False',
#               "tax": 'False'},
#              {"decription": 'matcha chess cake', "amount": '1', "price": 300, "total": 300, "voucher": 'False',
#               "tax": 'False'}
#          ]
#      },
#     {'id': "4", 'name': "hung", 'address': "Ha Tay", 'phone_number': "0987243623",
#      'email': "hung@boot.ai", 'total': 336, 'created': 1618440000, 'order':
#              {"decription": 'fruit chess cake', "amount": '1', "price": 168, "total": 168, "voucher": 'False',
#               "tax": 'False'},
#              {"decription": 'matcha chess cake', "amount": '1', "price": 168, "total": 168, "voucher": 'False',
#               "tax": 'False'}
#          ]
#      },
# ]

@api.route('/', methods=["POST"])
def create_recipe():
    data = reqparse.request.get_json()
    user = models.User(id=str(uuid.uuid1()), **data)
    try:
        user.save_to_db()
        return send_result(user.json())
    except:
        return send_error()


@api.route('', methods=['GET'])
def get_all():
    all_user = [x.json() for x in models.User.query.all()]
    for data in all_user:
        rs = []
        query = models.User.get_all_detail(data['id'])
        for i in query:
            result = {'description': i[1], 'amount': i[2], 'price': i[3], 'total': (i[2] * i[3])}
            rs.append(result)
        data["items"] = rs
    return send_result(data=all_user)


@api.route('/<string:input>', methods=['GET'])
def get_by_name(input):
    a = []
    all_user = [x.json() for x in models.User.query.all()]
    for data in all_user:
        rs = []
        query = models.User.get_all_detail(data['id'])
        for i in query:
            result = {'description': i[1], 'amount': i[2], 'price': i[3], 'total': (i[2] * i[3])}
            rs.append(result)
        data["items"] = rs

    for data in all_user:
        if data['username'] == input:
            a.append(data)
    return send_result(a)


@api.route('/date', methods=['GET'])
def get_by_date():
    a = []
    rs = []
    query = (models.User.query.join(models.Order, models.User.id == models.Order.user_id)
             .join(models.Order_detail, models.Order.id == models.Order_detail.order_id)
             .join(models.Item, models.Item.id == models.Order_detail.item_id)
             .add_columns(models.User.id, models.User.username, models.User.address, models.User.phone_number,
                          models.User.email, models.Item.name, models.Order_detail.amount, models.Item.price)).all()
    for i in query:
        result = {'id': i[1], 'name': i[2], 'address': i[3], 'phone_number': i[4], 'email': i[5],
                  'items': {'description': i[6], 'amount': i[7], 'price': i[8], 'total': (i[7] * i[8])}}
        rs.append(result)
    start = request.args.get('start', 1617210000, type=int)
    end = request.args.get('end', 1619715600, type=int)
    for data in rs:
        if data['created'] >= start and data['created'] <= end:
            a.append(data)
    return send_result(a)
