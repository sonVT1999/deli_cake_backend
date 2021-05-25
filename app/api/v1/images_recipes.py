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
        id_image = str(uuid.uuid1())
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            y = filename.split(".")
            filenames = y[0] + id_image + "." + y[-1]
            file.save(os.path.join(enums.UPLOAD_FOLDER2, filenames))
            image = models.Image_recipe(id=id_image, name=os.path.join(enums.SAVE_IMAGE_RECIPE, filenames),
                                        recipe_id=recipe_id)
            try:
                image.save_to_db()
                return send_result(image.json(), message="upload successfully!")
            except:
                return send_error()


@api.route('/create/', methods=["POST"])
def create_recipe():
    ingredient = request.form.get('ingredient')
    direction = request.form.getlist('direction')
    publish_at = request.form.get('publish_at')
    item_id = request.form.get('item_id')
    files = request.files.getlist("images")
    recipe = models.Recipe(id=str(uuid.uuid1()), direction=direction, ingredient=ingredient,
                           publish_at=publish_at, item_id=item_id)
    recipe.save_to_db()

    for file in files:
        if file and allowed_file(file.filename):
            id_image = str(uuid.uuid1())
            filename = secure_filename(file.filename)
            y = filename.split(".")
            filenames = y[0] + id_image + "." + y[-1]
            file.save(os.path.join(enums.UPLOAD_FOLDER2, filenames))
            image = models.Image_recipe(id=id_image, name=os.path.join(enums.SAVE_IMAGE_RECIPE, filenames),
                                        recipe_id=recipe.id)
            image.save_to_db()
    try:
        return send_result(recipe.json(), message="upload successfully!")
    except:
        return send_error()


@api.route('/', methods=['DELETE'])
def delete_by_id():
    _id = request.args.get('_id', type=str)
    image_recipe = models.Image_recipe.get_by_id(_id)
    if image_recipe:
        image_recipe.delete_to_db()
    return send_result(message="deleted successfully!")
