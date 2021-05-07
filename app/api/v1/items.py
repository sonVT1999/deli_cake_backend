from flask import Blueprint, request

from app import models
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
    x = [x.json() for x in models.Item.query.all()]

    for i in x:
        i["subcategory"] = models.Subcategory.get_by_id(i['id']).json()

    for i in x:
        i["category"] = models.Category.get_by_id(i['subcategory']['category_id']).json()

    return send_result(x)


@api.route('/<string:input>', methods=['GET'])
def search_by_id(input):
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
    global items
    ids = request.args.getlist('ids', type=str)
    items = [i for i in items if i["id"] not in ids]

    return send_result(items)


@api.route('/cate/<string:_id>', methods=['GET'])
def get_by_category(_id):
    sub_categories = models.Subcategory.get_by_id_category(_id)
    sub_category_ids = [i.id for i in sub_categories]
    _items = models.Item.query.filter(models.Item.subcategory_id.in_(sub_category_ids))
    rs = [i.json() for i in _items]
    for i in rs:
        i["subcategory"] = (models.Subcategory.get_by_id(i['subcategory_id'])).json()
    for i in rs:
        i["category"] = (models.Category.get_by_id(i['subcategory']['category_id'])).json()

    return send_result(rs)


@api.route('/sub/<string:_id>', methods=['GET'])
def get_by_sub(_id):
    x = [x.json() for x in models.Item.get_by_id_subcategory(_id)]

    for i in x:
        i["subcategory"] = (models.Subcategory.get_by_id(_id)).json()
        i["category"] = models.Category.get_by_id(i['subcategory']['category_id']).json()
    return send_result(x)
