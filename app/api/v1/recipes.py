import uuid

from flask import Blueprint, request
from flask_restful import reqparse

from app import models
from app.utils import send_result, send_error

api = Blueprint('recipes', __name__)


@api.route('/', methods=["POST"])
def create_recipe():
    data = reqparse.request.get_json()
    recipe = models.Recipe(id=str(uuid.uuid1()), **data)
    try:
        recipe.save_to_db()
        return send_result(recipe.json())
    except:
        return send_error()


@api.route('', methods=['GET'])
def get_all():
    rs = []
    query = models.Recipe.get_all_recipes()
    for i in query:
        result = {'id': i[1], 'title': i[2], 'publish_at': i[3], 'category': i[4], 'subcategory': i[5]}
        rs.append(result)
    return send_result(data=rs)


@api.route('/<string:input>', methods=['GET'])
def get_by_id(input):
    a = []
    rs = []
    query = models.Recipe.get_all_recipes()
    for i in query:
        result = {'id': i[1], 'title': i[2], 'publish_at': i[3], 'category': i[4], 'subcategory': i[5]}
        a.append(result)
    for data in a:
        if data['id'] == input or data['title'] == input:
            rs.append(data)
    return send_result(rs)


@api.route('/cate/<string:category>', methods=['GET'])
def get_by_category(category):
    a = []
    rs = []
    query = models.Recipe.get_all_recipes()
    for i in query:
        result = {'id': i[1], 'title': i[2], 'publish_at': i[3], 'category': i[4], 'subcategory': i[5]}
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
