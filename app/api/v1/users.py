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
#      }
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


