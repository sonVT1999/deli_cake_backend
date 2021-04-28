from flask import Blueprint

from app.utils import send_result

api = Blueprint('orders', __name__)

orders = [
    {'id': 1, 'total': 504, 'status': "completed", 'phone_number': "0123456789",
     'Address': "Ha Noi"},
    {'id': 2, 'total': 168, 'status': "pending", 'phone_number': "0123456789",
     'address': "Hai Phong"},
    {'id': 3, 'total': 257, 'status': "cancelled", 'phone_number': "0123456789",
     'address': "Thai Binh"}
]


@api.route('', methods=['GET'])
def get_all():
    return send_result(data=orders)
