import uuid

from flask import Blueprint
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
def create_user():
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
    # get user
    all_user = []
    query = models.User.get_all_user()
    for i in query:
        result = {'id': i[1], 'name': i[2], 'phone_number': i[3], 'email': i[4], 'total': i[5], 'voucher': i[6],
                  'tax': i[7]}
        all_user.append(result)

    # get order for user
    for data in all_user:
        rs = []
        query = models.User.get_all_detail(data['id'])
        for i in query:
            result = {'id': i[1], 'description': i[2], 'amount': i[3], 'price': i[4], 'total': (i[3] * i[4])}
            rs.append(result)
        data["items"] = rs

    # get order user by id_user or name_user
    a = []
    for data in all_user:
        if data['name'] == input or data['id'] == input:
            a.append(data)
    print(a)
    return send_result(a)
