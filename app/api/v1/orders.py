from flask import Blueprint, request


from app.utils import send_result, send_error

api = Blueprint('orders', __name__)

orders = [
    {'id': "1", 'total': 504, 'status': "completed", 'phone_number': "0123456789",
     'Address': "Ha Noi"},
    {'id': "2", 'total': 168, 'status': "pending", 'phone_number': "0123456789",
     'address': "Hai Phong"},
    {'id': "3", 'total': 257, 'status': "completed", 'phone_number': "0123456789",
     'address': "Thai Binh"},
    {'id': "4", 'total': 234, 'status': "confirmed", 'phone_number': "0123456789",
     'address': "Ha Nam"},
    {'id': "5", 'total': 856, 'status': "cancelled", 'phone_number': "0123456789",
     'address': "Quang Ninh"}
]


@api.route('', methods=['GET'])
def get_all():
    return send_result(data=orders)


@api.route('/stt/<string:status>', methods=['GET'])
def get_by_stt(status):
    i = []
    for data in orders:
        if data['status'] == status:
            i.append(data)
    return send_result(i)


@api.route('/<int:_id>', methods=['PUT'])
def put_by_id(_id):
    data = request.get_json()
    item = next(filter(lambda x: x['id'] == _id, orders), None)
    if item is None:
        send_error()
    else:
        keys = ["status"]
        for key in keys:
            if key in data.keys():
                item[key] = data[key]
        item.update(data)
    return send_result(item)


@api.route('/', methods=['DELETE'])
def delete_by_id():
    global orders

    ids = request.args.getlist('ids', type=str)
    orders = [u for u in orders if u["id"] not in ids]

    return send_result(orders)
