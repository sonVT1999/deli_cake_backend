import uuid

from flask import Blueprint, request
from flask_restful import reqparse

from app import models
from app.utils import send_result, send_error

api = Blueprint('recipes', __name__)

recipes = [
    {'id': "1", 'title': "galette des rois recipe", 'publish at': "4:00PM 12/01/2021", 'category': "birthday cake",
     'subcategory': "chiffon cake", 'ingredient': "", 'directions': "", 'image': ""},
    {'id': "2", 'title': "easter dove cake", 'publish at': "5:00PM 13/01/2021", 'category': "birthday cake",
     'subcategory': "key lime", 'ingredient': "", 'directions': "", 'image': ""},
    {'id': "3", 'title': "seven layer cake", 'publish at': "6:00PM 14/01/2021", 'category': "dessert cake",
     'subcategory': "pound cake", 'ingredient': "", 'directions': "", 'image': ""},
    {'id': "4", 'title': "seven layer cake", 'publish at': "5:00PM 20/01/2021", 'category': "dessert cake",
     'subcategory': "pound cake", 'ingredient': "", 'directions': "", 'image': ""}
]


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
    all_recipe = [x.json() for x in models.Recipe.query.all()]


@api.route('/<string:input>', methods=['GET'])
def get_by_id(input):
    i = []
    for data in recipes:
        if data['id'] == input or data['title'] == input:
            i.append(data)
    return send_result(i)


@api.route('/cate/<string:category>', methods=['GET'])
def get_by_category(category):
    i = []
    for data in recipes:
        if data['category'] == category:
            i.append(data)
    return send_result(i)


@api.route('/', methods=['DELETE'])
def delete_by_id():
    _id = request.args.get('id', type=str)
    item = models.Recipe.get_by_id(_id)
    if item:
        item.delete_to_db()
    return send_result(message="deleted successfully!")
