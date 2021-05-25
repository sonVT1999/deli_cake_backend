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
        id_image = str(uuid.uuid1())
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            y = filename.split(".")
            filenames = y[0] + id_image + "." + y[-1]
            file.save(os.path.join(enums.UPLOAD_FOLDER, filenames))
            image = models.Image_item(id=id_image, name=os.path.join(enums.SAVE_IMAGE_ITEM, filenames),
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
    files = request.files.getlist("images")
    item = models.Item(id=str(uuid.uuid1()), name=name, size=size, price=price, product_detail=product_detail,
                       subcategory_id=subcategory_id)
    item.save_to_db()

    for file in files:
        if file and allowed_file(file.filename):
            id_image = str(uuid.uuid1())
            filename = secure_filename(file.filename)
            y = filename.split(".")
            filenames = y[0] + id_image + "." + y[-1]
            file.save(os.path.join(enums.UPLOAD_FOLDER, filenames))
            image = models.Image_item(id=id_image, name=os.path.join(enums.SAVE_IMAGE_ITEM, filenames),
                                      item_id=item.id)
            image.save_to_db()
    try:
        return send_result(item.json(), message="upload successfully!")
    except:
        return send_error()


@api.route('/', methods=['DELETE'])
def delete_by_id():
    _id = request.args.get('_id', type=str)
    image_item = models.Image_item.get_by_id(_id)
    if image_item:
        image_item.delete_to_db()
    return send_result(message="deleted successfully!")
