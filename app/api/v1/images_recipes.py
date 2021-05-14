import os
import uuid

from flask import Blueprint, request
from werkzeug.utils import secure_filename

from app import enums, models
from app.utils import send_result, send_error

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

api = Blueprint('images_recipes', __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api.route('/<string:recipe_id>', methods=['GET', 'POST'])
def upload_file(recipe_id):
    if request.method == 'POST':
        if 'file' not in request.files:
            return send_error()
        file = request.files['file']
        if file.filename == '':
            return send_error()
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(enums.UPLOAD_FOLDER2, filename))
            image = models.Image_recipe(id=str(uuid.uuid1()), name=os.path.join(enums.SAVE_IMAGE_RECIPE, filename),
                                        recipe_id=recipe_id)
            try:
                image.save_to_db()
                return send_result(image.json(), message="upload successfully!")
            except:
                return send_error()