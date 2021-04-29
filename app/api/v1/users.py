from flask import Blueprint

from app.utils import send_result

api = Blueprint('users', __name__)

users = [
    {'id': "1", 'name': "son", 'address': "Ha Noi", 'phone_number': "0987243623",
     'email': "son@boot.ai", 'total': 504, 'created': "01/05/2021", 'order':
         [
             {"decription": 'matcha chess cake', "amount": '1', "price": 168, "total": 168, "voucher": 'False',
              "tax": 'False'},
             {"decription": 'matcha cake', "amount": '1', "price": 168, "total": 168, "voucher": 'False',
              "tax": 'False'},
             {"decription": 'chess cake', "amount": '1', "price": 168, "total": 168, "voucher": 'False',
              "tax": 'False'}
         ]
     },
    {'id': "2", 'name': "ha", 'address': "Thai Binh", 'phone_number': "0987243623",
     'email': "han@boot.ai", 'total': 668, 'created': "01/05/2021", 'order':
         [
             {"decription": 'matcha chess cake', "amount": '1', "price": 168, "total": 168, "voucher": 'False',
              "tax": 'False'},
             {"decription": 'chocolate chess cake', "amount": '1', "price": 100, "total": 100, "voucher": 'False',
              "tax": 'False'},
             {"decription": 'chocolate cake', "amount": '2', "price": 200, "total": 400, "voucher": 'False',
              "tax": 'False'}
         ]
     },
    {'id': "3", 'name': "hao", 'address': "Ha Nam", 'phone_number': "0987243623",
     'email': "hao@boot.ai", 'total': 600, 'created': "01/05/2021", 'order':
         [
             {"decription": 'banana cake', "amount": '1', "price": 100, "total": 100, "voucher": 'False',
              "tax": 'False'},
             {"decription": 'pine chess cake', "amount": '1', "price": 200, "total": 200, "voucher": 'False',
              "tax": 'False'},
             {"decription": 'matcha chess cake', "amount": '1', "price": 300, "total": 300, "voucher": 'False',
              "tax": 'False'}
         ]
     },
    {'id': "4", 'name': "hung", 'address': "Ha Tay", 'phone_number': "0987243623",
     'email': "hung@boot.ai", 'total': 504, 'created': "01/05/2021", 'order':
         [
             {"decription": 'fruit chess cake', "amount": '1', "price": 168, "total": 168, "voucher": 'False',
              "tax": 'False'},
             {"decription": 'matcha chess cake', "amount": '1', "price": 168, "total": 168, "voucher": 'False',
              "tax": 'False'},
             {"decription": 'chocolate cake', "amount": '1', "price": 168, "total": 168, "voucher": 'False',
              "tax": 'False'}
         ]
     },
]


@api.route('', methods=['GET'])
def get_all():
    return send_result(data=users)


@api.route('/<string:input>', methods=['GET'])
def get_by_name(input):
    i = []
    for data in users:
        if data['name'] == input:
            i.append(data)
    return send_result(i)