from flask import Blueprint, request

from app.utils import send_result, send_error

api = Blueprint('items', __name__)

items = [
    {'id': "1", 'name': "matcha chess cake", 'price': 40, 'category': "birthday cake",
     'subcategory': "chiffon cake"},
    {'id': "2", 'name': "yellow chess cake", 'price': 36, 'category': "birthday cake",
     'subcategory': "key lime"},
    {'id': "3", 'name': "chocolate chess cake", 'price': 32, 'category': "dessert cake",
     'subcategory': "pound cake"}
]


@api.route('/', methods=["POST"])
def create_item():

    data = request.get_json()
    item = {**data}
    items.append(item)
    try:
        return send_result(item)
    except:
        return send_error()


@api.route('', methods=['GET'])
def get_all():
    return send_result(data=items)


@api.route('/<string:input>', methods=['GET'])
def get_by_id(input):
    i = []
    for data in items:
        if data['id'] or data['name'] == input:
            i.append(data)
    return send_result(i)


@api.route('/<int:_id>', methods=['PUT'])
def put_by_id(_id):
    data = request.get_json()
    item = next(filter(lambda x: x['id'] == _id, items), None)
    if item is None:
        send_error()
    else:
        keys = ["name", "price", "category", "subcategory"]
        for key in keys:
            if key in data.keys():
                item[key] = data[key]
        item.update(data)
    return send_result(item)


@api.route('/', methods=['DELETE'])
def delete_by_id():

    # list1 = [
    #     {'id': 1, "name": "abc"},
    #     {'id': 2, "name": "3abc"},
    #     {'id': 3, "name": "2abc"},
    # ]
    #
    # ids = [1, 2]
    #
    # new_list = [
    #     {'id': 3, "name": "2abc"}
    # ]

    # for i in ids:
    #     try:
    #         list1.remove(i)
    #     except ValueError:
    #         pass

    # set1 = set(list1)
    # set2 = set(ids)
    # res = list(set1 - set2)

    im = []
    ids = request.args.getlist("ids")
    for data in items:
        if data['id'] == ids:
            im.append(data)
    res = filter(lambda i: i not in im, items)
    #  cap nhat bien toan cuc
    return send_result(items)


@api.route('/cate/<string:category>', methods=['GET'])
def get_by_category(category):
    i = []
    for data in items:
        if data['category'] == category:
            i.append(data)
    return send_result(i)


@api.route('/sub', methods=['GET'])
def get_by_sub():
    i = []
    cate = request.args.get('cate', "", type=str)
    sub = request.args.get('sub', "", type=str)
    for data in items:
        if data['category'] == cate and data['subcategory'] == sub:
            i.append(data)
    return send_result(i)
