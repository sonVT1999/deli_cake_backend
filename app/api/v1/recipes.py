from flask import Blueprint, request

from app import models
from app.utils import send_result

api = Blueprint('recipes', __name__)


@api.route('', methods=['GET'])
def get_all():
    result = []
    num_page = request.args.get('num_page', type=int)
    query = models.Recipe.get_recipes_paginate(num_page)
    for i in query:
        rs = {'id': i[1], 'name_cake': i[2], 'publish_at': i[3], 'category_id': i[4], 'category': i[5],
              'subcategory_id': i[6], 'subcategory': i[7]}
        result.append(rs)

    for data in result:
        data["images_recipes"] = [x.json() for x in models.Image_recipe.get_by_id_recipe(data['id'])]

    return send_result(data=result)


@api.route('/<string:input>', methods=['GET'])
def get_by_id(input):
    recipe = []
    result = []

    query = models.Recipe.get_all_recipes()
    for i in query:
        rs = {'id': i[1], 'name_cake': i[2], 'publish_at': i[3], 'direction': i[4], 'ingredient': i[5],
              'category_id': i[6], 'category': i[7], 'subcategory_id': i[8], 'subcategory': i[9]}
        result.append(rs)

    for data in result:
        data["images_recipes"] = [x.json() for x in models.Image_recipe.get_by_id_recipe(data['id'])]

    for data in result:
        if data['id'] == input or data['name_cake'] == input:
            recipe.append(data)
    return send_result(recipe)


# @api.route('/<string:_id>', methods=['PUT'])
# def put_by_id(_id):
#     data = reqparse.request.get_json()
#
#     item = models.Item.find_by_id(_id)
#     if item is None:
#         send_error()
#     else:
#         keys = ["name", "price", "product_detail", "size", "subcategory"]
#         for key in keys:
#             if key in data.keys():
#                 setattr(item, key, data[key])
#         db.session.commit()
#     return send_result(item.json())


@api.route('/cate/<string:category>', methods=['GET'])
def get_by_category(category):
    a = []
    rs = []
    query = models.Recipe.get_all_recipes()
    for i in query:
        result = {'id': i[1], 'name_cake': i[2], 'publish_at': i[3], 'category_id': i[6], 'category': i[7],
                  'subcategory_id': i[8], 'subcategory': i[9]}
        a.append(result)
    for data in a:
        if data['category'] == category:
            rs.append(data)
    return send_result(rs)


@api.route('/', methods=['DELETE'])
def delete_by_id():
    _id = request.args.get('id', type=str)
    recipe = models.Recipe.get_by_id(_id)
    if recipe:
        recipe.delete_to_db()
    return send_result(message="deleted successfully!")
