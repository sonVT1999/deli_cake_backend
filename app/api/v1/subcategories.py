from flask import Blueprint, request

from app.utils import send_result, send_error

api = Blueprint('subcategories', __name__)

subcategory = [
            {"id": "1", "name": "chiffon cake", "category_name": "birthday cake"},
            {"id": "2", "name": "pound cake", "category_name": "cheese cake"},
            ]


@api.route('', methods=['GET'])
def get_all():
    return send_result(data=subcategory)


@api.route('/', methods=["POST"])
def create_cate():
    data = request.get_json()
    cate = {**data}
    subcategory.append(cate)
    try:
        return send_result(cate)
    except:
        return send_error()