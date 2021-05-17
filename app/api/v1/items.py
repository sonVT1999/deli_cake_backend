
from flask import Blueprint
from flask_restful import request, reqparse

from app import models
from app.extensions import db
from app.utils import send_result, send_error

api = Blueprint('items', __name__)


@api.route('', methods=['GET'])
def get_all():
    result = []
    query = models.Item.get_all_item()
    for i in query:
        rs = {'id': i[1], 'name': i[2], 'price': i[3], 'product_detail': i[4], 'size': i[5],
              'subcategory_id': i[6], 'subcategory': i[7], 'category_id': i[8], 'category': i[9]}
        result.append(rs)

    for data in result:
        data["images_items"] = [x.json() for x in models.Image_item.get_by_id_item(data['id'])]
    return send_result(data=result)


@api.route('/<string:input>', methods=['GET'])
def search_by_id(input):
    item = []
    result = []

    query = models.Item.get_all_item()
    for i in query:
        rs = {'id': i[1], 'name': i[2], 'price': i[3], 'product_detail': i[4], 'size': i[5],
              'subcategory_id': i[6], 'subcategory': i[7], 'category_id': i[8], 'category': i[9]}
        result.append(rs)

    for data in result:
        data["images_items"] = [x.json() for x in models.Image_item.get_by_id_item(data['id'])]

    for data in result:
        if data['id'] == input or data['name'] == input:
            item.append(data)
    return send_result(item)


@api.route('/<string:_id>', methods=['PUT'])
def put_by_id(_id):
    data = reqparse.request.get_json()

    item = models.Item.find_by_id(_id)
    if item is None:
        send_error()
    else:
        keys = ["name", "price", "product_detail", "size", "subcategory"]
        for key in keys:
            if key in data.keys():
                setattr(item, key, data[key])
        db.session.commit()
    return send_result(item.json())


@api.route('/', methods=['DELETE'])
def delete_by_id():
    ids = request.args.getlist('ids', type=str)
    for i in ids:
        item = models.Item.find_by_id(i)
        if item:
            item.delete_to_db()
    return send_result(message="deleted successfully!")


@api.route('/cate/<string:_id>', methods=['GET'])
def get_by_category(_id):
    # sub_categories = models.Subcategory.get_by_id_category(_id)
    # sub_category_ids = [i.id for i in sub_categories]
    # _items = models.Item.query.filter(models.Item.subcategory_id.in_(sub_category_ids))
    # rs = [i.json() for i in _items]
    # for data in rs:
    #     data["subcategory"] = (models.Subcategory.get_by_id(data['subcategory_id'])).json()
    # for data in rs:
    #     data["category"] = (models.Category.get_by_id(data['subcategory']['category_id'])).json()
    item = []
    result = []

    query = models.Item.get_all_item()
    for i in query:
        rs = {'id': i[1], 'name': i[2], 'price': i[3], 'product_detail': i[4], 'size': i[5],
              'subcategory_id': i[6], 'subcategory': i[7], 'category_id': i[8], 'category': i[9]}
        result.append(rs)

    for data in result:
        data["images_items"] = [x.json() for x in models.Image_item.get_by_id_item(data['id'])]

    for data in result:
        if data['category_id'] == _id:
            item.append(data)
    return send_result(item)


@api.route('/sub/<string:_id>', methods=['GET'])
def get_by_sub(_id):
    # rs = [x.json() for x in models.Item.get_by_id_subcategory(_id)]
    #
    # for data in rs:
    #     data["subcategory"] = (models.Subcategory.get_by_id(_id)).json()
    #     data["category"] = models.Category.get_by_id(data['subcategory']['category_id']).json()
    # return send_result(rs)
    item = []
    result = []

    query = models.Item.get_all_item()
    for i in query:
        rs = {'id': i[1], 'name': i[2], 'price': i[3], 'product_detail': i[4], 'size': i[5],
              'subcategory_id': i[6], 'subcategory': i[7], 'category_id': i[8], 'category': i[9]}
        result.append(rs)

    for data in result:
        data["images_items"] = [x.json() for x in models.Image_item.get_by_id_item(data['id'])]

    for data in result:
        if data['subcategory_id'] == _id:
            item.append(data)
    return send_result(item)
