from flask import Blueprint, request

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
    data = request.get_json()
    recipe = {**data}
    recipes.append(recipe)
    try:
        return send_result(recipe)
    except:
        return send_error()


@api.route('', methods=['GET'])
def get_all():
    return send_result(data=recipes)


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

    global recipes
    ids = request.args.getlist('ids', type=list)
    recipes = [i for i in recipes if i["id"] not in ids]

    return send_result(recipes)
