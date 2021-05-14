import os
import uuid

from flask import Blueprint, request
from werkzeug.utils import secure_filename

from app import enums, models
from app.utils import send_result, send_error

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

api = Blueprint('images_items', __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api.route('/<string:item_id>', methods=['GET', 'POST'])
def upload_file(item_id):
    if request.method == 'POST':
        if 'file' not in request.files:
            return send_error()
        file = request.files['file']
        if file.filename == '':
            return send_error()
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(enums.UPLOAD_FOLDER, filename))
            image = models.Image_item(id=str(uuid.uuid1()), name=os.path.join(enums.SAVE_IMAGE_ITEM, filename),
                                      item_id=item_id)
            try:
                image.save_to_db()
                return send_result(image.json(), message="upload successfully!")
            except:
                return send_error()


@api.route('/create/', methods=["POST"])
def create_item():
    name = request.form.get('name')
    size = request.form.get('size')
    price = request.form.get('price')
    product_detail = request.form.get('product_detail')
    subcategory_id = request.form.get('subcategory_id')
    file = request.files['file']
    item = models.Item(id=str(uuid.uuid1()), name=name, size=size, price=price, product_detail=product_detail,
                       subcategory_id=subcategory_id)
    item.save_to_db()

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(enums.UPLOAD_FOLDER, filename))
        image = models.Image_item(id=str(uuid.uuid1()), name=os.path.join(enums.SAVE_IMAGE_ITEM, filename),
                                  item_id=item.id)
        image.save_to_db()
    try:
        return send_result(item.json(), message="upload successfully!")
    except:
        return send_error()
