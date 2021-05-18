from flask import Blueprint

from app import models
from app.utils import send_result

api = Blueprint('categories', __name__)

# categories = [
#     {'id': 1, 'name': "birthday cake",
#      'subcategory':
#          [
#              {
#                  "sub_id": 1,
#                  "sub_name": "chiffon cake"
#              },
#              {
#                  "sub_id": 2,
#                  "sub_name": "pound cake"
#              },
#              {
#                  "sub_id": 3,
#                  "sub_name": "fruit cake"
#              }
#          ]
#      }
# ]


@api.route('', methods=['GET'])
def get_all():
    t = [x.json() for x in models.Category.query.all()]
    for i in t:
        i["subcategory"] = [x.json() for x in models.Subcategory.get_by_id_category(i['id'])]
    return send_result(t)
