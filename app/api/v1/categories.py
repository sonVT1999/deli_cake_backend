from flask import Blueprint, request

from app import models
from app.utils import send_result, send_error

api = Blueprint('categories', __name__)

categories = [
    {'id': "1", 'name': "birthday cake",
     'subcategory':
         [
             {
                 "sub_id": 1,
                 "sub_name": "chiffon cake"
             },
             {
                 "sub_id": 2,
                 "sub_name": "pound cake"
             },
             {
                 "sub_id": 3,
                 "sub_name": "fruit cake"
             }
         ]
     },

    {'id': "2", 'name': "cheese cake",
     'subcategory':
         [
             {
                 "sub_id": 1,
                 "sub_name": "pumpkin cheesecake"
             },
             {
                 "sub_id": 2,
                 "sub_name": "chocolate"
             },
             {
                 "sub_id": 3,
                 "sub_name": "key lime"
             }
         ]
     },
    {'id': "3", 'name': "dessert cake", 'subcategory':
        [
            {
                "sub_id": 1,
                "sub_name": "pound cake"
            },
            {
                "sub_id": 2,
                "sub_name": "carrot cake"
            },
            {
                "sub_id": 3,
                "sub_name": "chocolate chip cookies"
            }
        ]
     },
    {'id': "4", 'name': "bread", 'subcategory':
        [
            {
                "sub_id": 1,
                "sub_name": "rye bread"
            },
            {
                "sub_id": 2,
                "sub_name": "pita bread"
            },
            {
                "sub_id": 3,
                "sub_name": "multigrain"
            }
        ]
     }
]


@api.route('', methods=['GET'])
def get_all():

    t = [x.json() for x in models.Category.query.all()]
    for i in t:
        i["subcategory"] = [x.json() for x in models.Subcategory.get_by_id_category(i['id'])]
    return send_result(t)

